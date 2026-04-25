"""
Agent service that uses Azure OpenAI function calling (if configured)
to determine which local skill to call. It provides a fallback parser
if OpenAI is not configured.
"""
import json
import logging
import re
from dotenv import load_dotenv
from .config import Config
from .skills import db_skills, po_skill

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    openai = None
    OPENAI_AVAILABLE = False

OPENAI_FUNCTIONS = [
    {
        "name": "get_po_status",
        "description": "Get status and basic info for a purchase order",
        "parameters": {
            "type": "object",
            "properties": {"po_number": {"type": "string"}},
            "required": ["po_number"]
        }
    },
    {
        "name": "list_pos_by_vendor",
        "description": "List purchase orders for a vendor",
        "parameters": {
            "type": "object",
            "properties": {"vendor_code": {"type": "string"}},
            "required": ["vendor_code"]
        }
    },
    {
        "name": "get_vendor_info",
        "description": "Get vendor details",
        "parameters": {
            "type": "object",
            "properties": {"vendor_code": {"type": "string"}},
            "required": ["vendor_code"]
        }
    },
    {
        "name": "get_open_pos",
        "description": "Return a list of open purchase orders",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "create_po",
        "description": "Create a purchase order with vendor_code and items",
        "parameters": {
            "type": "object",
            "properties": {
                "vendor_code": {"type": "string"},
                "items": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["vendor_code", "items"]
        }
    },
    {
        "name": "list_vendors",
        "description": "List all vendors",
        "parameters": {"type": "object", "properties": {}}
    }
]

def call_local_function(name, args):
    if name == "get_po_status":
        return db_skills.skill_get_po_status(args.get("po_number"))

    if name == "list_pos_by_vendor":
        return db_skills.skill_list_pos_by_vendor(args.get("vendor_code"))

    if name == "get_vendor_info":
        return db_skills.skill_get_vendor_info(args.get("vendor_code"))

    if name == "get_open_pos":
        return db_skills.skill_get_open_pos()

    if name == "create_po":
        return po_skill.skill_create_po(
            args.get("vendor_code"),
            args.get("items")
        )

    if name == "list_vendors":
        return db_skills.skill_list_vendors()

    return {"error": True, "message": "Unknown function"}


def summarize(intent, data):
    if isinstance(data, dict) and data.get("error"):
        return data.get("message", "An error occurred.")

    if intent == "LIST_VENDORS":
        return (
            "There are currently no vendors registered."
            if not data else
            f"There are {len(data)} vendors registered."
        )

    if intent == "GET_PO_STATUS":
        return (
            f"Purchase order {data['po_number']} is "
            f"{data['status']} with a total of "
            f"{data['currency']} {data['total_amount']}."
        )

    if intent == "LIST_OPEN_POS":
        return (
            "There are no open purchase orders."
            if not data else
            f"There are {len(data)} open purchase orders."
        )

    if intent == "LIST_VENDOR_POS":
        return (
            "This vendor has no purchase orders."
            if not data else
            f"This vendor has {len(data)} purchase orders."
        )

    if intent == "GET_VENDOR_INFO":
        return f"Vendor {data['code']} is registered and active."

    return "Request completed successfully."

def run_agent(prompt: str):

    azure_ready = (
        OPENAI_AVAILABLE and
        Config.OPENAI_API_KEY and
        Config.AZURE_OPENAI_ENDPOINT and
        Config.AZURE_OPENAI_DEPLOYMENT and
        Config.AZURE_OPENAI_API_VERSION
    )

    if azure_ready:
        try:
            openai.api_type = "azure"
            openai.api_base = Config.AZURE_OPENAI_ENDPOINT
            openai.api_version = Config.AZURE_OPENAI_API_VERSION
            openai.api_key = Config.OPENAI_API_KEY

            resp = openai.ChatCompletion.create(
                engine=Config.AZURE_OPENAI_DEPLOYMENT,
                messages=[{"role": "user", "content": prompt}],
                functions=OPENAI_FUNCTIONS,
                function_call="auto",
                temperature=0.0
            )

            msg = resp["choices"][0]["message"]

            if msg.get("function_call"):
                func = msg["function_call"]["name"]
                args = json.loads(msg["function_call"].get("arguments") or "{}")
                data = call_local_function(func, args)
                intent = func.upper()

                return {
                    "type": "function_result",
                    "intent": intent,
                    "confidence": "high",
                    "summary": summarize(intent, data),
                    "data": data
                }

            return {
                "type": "message",
                "confidence": "medium",
                "content": msg.get("content", "")
            }

        except Exception:
            logger.exception("Azure OpenAI failed, falling back")

    # ---------------- FALLBACK PARSER ----------------
    lower = prompt.lower()

    if "vendor" in lower and any(w in lower for w in ["list", "show", "all"]):
        data = call_local_function("list_vendors", {})
        return {
            "type": "function_result",
            "intent": "LIST_VENDORS",
            "confidence": "high",
            "summary": summarize("LIST_VENDORS", data),
            "data": data
        }

    po_match = re.search(r"(po[a-z0-9-]+)", prompt, re.IGNORECASE)
    if po_match:
        data = call_local_function(
            "get_po_status",
            {"po_number": po_match.group(1).upper()}
        )
        return {
            "type": "function_result",
            "intent": "GET_PO_STATUS",
            "confidence": "high",
            "summary": summarize("GET_PO_STATUS", data),
            "data": data
        }

    if "open" in lower and "po" in lower:
        data = call_local_function("get_open_pos", {})
        return {
            "type": "function_result",
            "intent": "LIST_OPEN_POS",
            "confidence": "high",
            "summary": summarize("LIST_OPEN_POS", data),
            "data": data
        }

    vendor_match = re.search(r"vendor\s+([A-Za-z0-9_-]+)", prompt, re.IGNORECASE)
    if vendor_match:
        data = call_local_function(
            "list_pos_by_vendor",
            {"vendor_code": vendor_match.group(1)}
        )
        return {
            "type": "function_result",
            "intent": "LIST_VENDOR_POS",
            "confidence": "high",
            "summary": summarize("LIST_VENDOR_POS", data),
            "data": data
        }

    return {
        "type": "message",
        "confidence": "low",
        "content": (
            "I couldn’t determine a clear action. "
            "Try: 'list vendors', 'show open POs', or 'status PO1234'."
        )
    }
