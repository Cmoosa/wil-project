from flask import Blueprint, request, jsonify, current_app
from ..json_db import list_vendors, create_vendor, get_vendor_by_code
from ..models import make_vendor

bp = Blueprint("vendor", __name__, url_prefix="/api/vendor")

@bp.route("/", methods=["GET"])
def list_all():
    path = current_app.config.get("DB_PATH")
    vendors = list_vendors(path)
    return jsonify(vendors), 200

@bp.route("/", methods=["POST"])
def create():
    data = request.get_json() or {}
    code = data.get("code")
    name = data.get("name")
    contact_email = data.get("contact_email")
    if not code or not name:
        return jsonify({"error": "code and name required"}), 400
    try:
        vendor_obj = make_vendor(code, name, contact_email)
        created = create_vendor(current_app.config.get("DB_PATH"), vendor_obj)
        return jsonify(created), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
