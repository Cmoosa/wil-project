from flask import Blueprint, request, jsonify
from app.agent_service import run_agent

bp = Blueprint("agent", __name__, url_prefix="/api/agent")

@bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "prompt required"}), 400

    result = run_agent(prompt)

    if result["type"] == "error":
        return jsonify(result), 500

    return jsonify(result), 200
