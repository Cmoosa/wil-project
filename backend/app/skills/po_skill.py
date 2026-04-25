import uuid
from ..json_db import create_po
from ..config import Config

def skill_create_po(vendor_code, items):
    po_number = f"PO{uuid.uuid4().hex[:8].upper()}"
    total = sum(i["qty"] * i["unit_price"] for i in items)

    po = {
        "po_number": po_number,
        "vendor_code": vendor_code,
        "items": items,
        "total_amount": total,
        "currency": "ZAR"
    }

    return create_po(Config.DB_PATH, po)
