from flask import Blueprint, request, jsonify, current_app
from ..models import make_po
from ..json_db import get_po_by_number, create_po, get_vendor_by_code

bp = Blueprint("po", __name__, url_prefix="/api/po")

@bp.route("/<string:po_number>", methods=["GET"])
def get_po(po_number):
    path = current_app.config.get("DB_PATH")
    po = get_po_by_number(path, po_number)
    if not po:
        return jsonify({"error": "PO not found", "status": "PO_NOT_FOUND"}), 404
    return jsonify(po), 200

@bp.route("/", methods=["POST"])
def create_po_route():
    data = request.get_json(force=True) or {}
    vendor_code = data.get("vendorCode")
    items = data.get("items", [])
    if not vendor_code or not items:
        return jsonify({"error": "vendorCode and items required"}), 400
    path = current_app.config.get("DB_PATH")
    vendor = get_vendor_by_code(path, vendor_code)
    if not vendor:
        return jsonify({"error": "vendor not found"}), 404
    po_obj = make_po(vendor_code, items)
    created = create_po(path, po_obj)
    return jsonify(created), 201
