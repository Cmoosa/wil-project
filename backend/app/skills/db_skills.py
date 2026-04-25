
"""
Skills that the agent can call which operate on the JSON DB.
All skills return JSON-serializable dicts or lists.
"""

from ..json_db import (
    get_vendor_by_code,
    get_po_by_number,
    list_pos,
    list_open_pos,
    list_vendors,
)
from ..config import Config

def skill_list_vendors():
    """
    List all vendors in the system.
    """
    path = Config.DB_PATH
    return list_vendors(path)


def skill_get_vendor_info(vendor_code):
    """
    Get details for a single vendor.
    """
    path = Config.DB_PATH
    vendor = get_vendor_by_code(path, vendor_code)

    if not vendor:
        return {"error": f"No vendor found with code {vendor_code}"}

    return {
        "code": vendor.get("code"),
        "name": vendor.get("name"),
        "contact_email": vendor.get("contact_email"),
    }


def skill_get_po_status(po_number):
    """
    Get the status of a specific purchase order.
    """
    path = Config.DB_PATH
    po = get_po_by_number(path, po_number)

    if not po:
        return {"error": f"No purchase order found with number {po_number}"}

    return {
        "po_number": po.get("po_number"),
        "vendor_code": po.get("vendor_code"),
        "status": po.get("status"),
        "total_amount": po.get("total_amount"),
        "currency": po.get("currency", "ZAR"),
        "created_at": po.get("created_at"),
    }


def skill_list_pos_by_vendor(vendor_code):
    """
    List all purchase orders for a given vendor.
    """
    path = Config.DB_PATH

    vendor = get_vendor_by_code(path, vendor_code)
    if not vendor:
        return {"error": f"No vendor found with code {vendor_code}"}

    pos = [
        p for p in list_pos(path)
        if p.get("vendor_code") == vendor_code
    ]

    return [
        {
            "po_number": p.get("po_number"),
            "status": p.get("status"),
            "total_amount": p.get("total_amount"),
            "created_at": p.get("created_at"),
        }
        for p in pos
    ]


def skill_get_open_pos():
    """
    List all open purchase orders.
    """
    path = Config.DB_PATH
    pos = list_open_pos(path)

    return [
        {
            "po_number": p.get("po_number"),
            "vendor_code": p.get("vendor_code"),
            "total_amount": p.get("total_amount"),
        }
        for p in pos
    ]
"""
Skills that the agent can call which operate on the JSON DB.
All skills return JSON-serializable dicts or lists.
Enterprise rule: NEVER return None.
"""

from ..json_db import (
    get_vendor_by_code,
    get_po_by_number,
    list_pos,
    list_open_pos,
    list_vendors,
)
from ..config import Config


def skill_list_vendors():
    """
    List all vendors in the system.
    Always returns a list.
    """
    path = Config.DB_PATH
    vendors = list_vendors(path)

    if not vendors:
        return [] 
    
    return [
        {
            "code": v.get("code"),
            "name": v.get("name"),
            "contact_email": v.get("contact_email"),
        }
        for v in vendors
    ]


def skill_get_vendor_info(vendor_code):
    """
    Get details for a single vendor.
    Returns a dict.
    """
    path = Config.DB_PATH
    vendor = get_vendor_by_code(path, vendor_code)

    if not vendor:
        return {
            "error": True,
            "message": f"No vendor found with code {vendor_code}"
        }

    return {
        "code": vendor.get("code"),
        "name": vendor.get("name"),
        "contact_email": vendor.get("contact_email"),
    }


def skill_get_po_status(po_number):
    """
    Get the status of a specific purchase order.
    Returns a dict.
    """
    path = Config.DB_PATH
    po = get_po_by_number(path, po_number)

    if not po:
        return {
            "error": True,
            "message": f"No purchase order found with number {po_number}"
        }

    return {
        "po_number": po.get("po_number"),
        "vendor_code": po.get("vendor_code"),
        "status": po.get("status"),
        "total_amount": po.get("total_amount"),
        "currency": po.get("currency", "ZAR"),
        "created_at": po.get("created_at"),
    }


def skill_list_pos_by_vendor(vendor_code):
    """
    List all purchase orders for a given vendor.
    Always returns a list.
    """
    path = Config.DB_PATH
    vendor = get_vendor_by_code(path, vendor_code)

    if not vendor:
        return [] 

    pos = [
        p for p in list_pos(path)
        if p.get("vendor_code") == vendor_code
    ]

    if not pos:
        return []

    return [
        {
            "po_number": p.get("po_number"),
            "status": p.get("status"),
            "total_amount": p.get("total_amount"),
            "created_at": p.get("created_at"),
        }
        for p in pos
    ]


def skill_get_open_pos():
    """
    List all open purchase orders.
    Always returns a list.
    """
    path = Config.DB_PATH
    pos = list_open_pos(path)

    if not pos:
        return []

    return [
        {
            "po_number": p.get("po_number"),
            "vendor_code": p.get("vendor_code"),
            "total_amount": p.get("total_amount"),
        }
        for p in pos
    ]
