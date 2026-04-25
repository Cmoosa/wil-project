import uuid
import datetime
from decimal import Decimal

def make_vendor(code, name, contact_email=None, phone=None):
    return {
        "id": str(uuid.uuid4()),
        "code": code,
        "name": name,
        "contact_email": contact_email,
        "phone": phone,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

def make_po(vendor_code, items, currency="ZAR"):
    # items is list of {description, qty, unit_price}
    total = Decimal("0.00")
    lines = []
    for it in items:
        qty = int(it.get("qty", 1))
        unit_price = Decimal(str(it.get("unit_price", 0)))
        lines.append({
            "description": it.get("description", ""),
            "qty": qty,
            "unit_price": float(unit_price)
        })
        total += unit_price * qty

    return {
        "po_number": f"PO{uuid.uuid4().hex[:8].upper()}",
        "vendor_code": vendor_code,
        "total_amount": float(total),
        "currency": currency,
        "status": "PO_CREATED",
        "lines": lines,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }
