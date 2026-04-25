import jwt
import os
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict
from functools import wraps
from flask import request, jsonify, current_app

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 60


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 100_000
    )
    return f"{salt.hex()}${pwd_hash.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, hash_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, 100_000
        )
        return hmac.compare_digest(pwd_hash, expected)
    except Exception:
        return False

import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_token(user):
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "role": user.get("role", "user"),
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def decode_token(token: str) -> Dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

def public_user(user: Dict) -> Dict:
    return {
        "email": user["email"],
        "role": user.get("role", "user"),
        "created_at": user.get("created_at"),
    }

def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({"error": "Unauthorized"}), 401

            token = auth.split(" ")[1]

            try:
                payload = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except Exception:
                return jsonify({"error": "Invalid token"}), 401

            if payload.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403

            request.user = payload
            return fn(*args, **kwargs)

        return wrapper
    return decorator
