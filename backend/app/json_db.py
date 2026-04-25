import json
import os
from datetime import datetime
from .constants.po_lifecycle import ALLOWED_TRANSITIONS, OPEN_STATUSES

def init_db(path):
    """
    Ensure the JSON database exists and has the correct structure.
    """
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(
                {
                    "vendors": [],
                    "purchase_orders": [],
                    "po_events": []
                },
                f,
                indent=2
            )
            
def _read_db(path):
    if not os.path.exists(path):
        return {
            "users": [],
            "vendors": [],
            "purchase_orders": [],
            "po_events": [],
        }
    with open(path, "r") as f:
        return json.load(f)

def _write_db(path, db):
    with open(path, "w") as f:
        json.dump(db, f, indent=2)

# ---------------- USERS ----------------

def list_users(path):
    return _read_db(path).get("users", [])

# -------------------------------------------------
# USERS (AUTH)
# -------------------------------------------------

def _load_db(path):
    if not os.path.exists(path):
        return {
            "vendors": [],
            "purchase_orders": [],
            "po_events": [],
            "users": []
        }
    with open(path, "r") as f:
        return json.load(f)


def _save_db(path, db):
    with open(path, "w") as f:
        json.dump(db, f, indent=2)


def get_user_by_email(path, email):
    db = _load_db(path)
    return next((u for u in db.get("users", []) if u["email"] == email), None)


def create_user(path, user):
    db = _load_db(path)

    if get_user_by_email(path, user["email"]):
        raise ValueError("User already exists")

    db.setdefault("users", []).append(user)
    _save_db(path, db)
    return user


# ---------------- Vendors ----------------

def list_vendors(path):
    return _read_db(path).get("vendors", [])

def get_vendor_by_code(path, code):
    return next((v for v in list_vendors(path) if v["code"] == code), None)

def create_vendor(path, vendor):
    db = _read_db(path)
    if get_vendor_by_code(path, vendor["code"]):
        raise ValueError("Vendor already exists")
    db["vendors"].append(vendor)
    _write_db(path, db)
    return vendor

# ---------------- Purchase Orders ----------------

def create_po(path, po):
    db = _read_db(path)

    po["status"] = "PO_DRAFT"
    po["created_at"] = datetime.utcnow().isoformat()

    db["purchase_orders"].append(po)
    db["po_events"].append({
        "po_number": po["po_number"],
        "event": "CREATED",
        "status": "PO_DRAFT"
    })

    _write_db(path, db)
    return po

def list_pos(path):
    return _read_db(path).get("purchase_orders", [])

def get_po_by_number(path, po_number):
    return next((p for p in list_pos(path) if p["po_number"] == po_number), None)

def list_open_pos(path):
    return [p for p in list_pos(path) if p["status"] in OPEN_STATUSES]

def update_po_status(path, po_number, new_status):
    db = _read_db(path)
    po = get_po_by_number(path, po_number)

    if not po:
        raise ValueError("PO not found")

    current = po["status"]
    if new_status not in ALLOWED_TRANSITIONS.get(current, []):
        raise ValueError(f"Invalid transition {current} → {new_status}")

    po["status"] = new_status
    po["updated_at"] = datetime.utcnow().isoformat()

    db["po_events"].append({
        "po_number": po_number,
        "event": "STATUS_CHANGE",
        "from": current,
        "to": new_status
    })

    _write_db(path, db)
    return po
