import requests
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

from ..json_db import create_user, get_user_by_email
from ..utils.auth import hash_password, verify_password, public_user
from ..utils.jwt import generate_token

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

N8N_SIGNUP_WEBHOOK = "https://vyingly-grainless-fernande.ngrok-free.dev/webhook-test/notifications"

@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if get_user_by_email(current_app.config["DB_PATH"], email):
        return jsonify({"error": "User already exists"}), 409

    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": hash_password(password),
        "role": "buyer",
        "created_at": datetime.utcnow().isoformat(),
    }

    create_user(current_app.config["DB_PATH"], user)

    try:
        requests.post(
            N8N_SIGNUP_WEBHOOK,
            json={
                "event": "signup_success",
                "user": public_user(user),
            },
            timeout=3,
        )
    except Exception:
        pass

    return jsonify({
        "message": "Signup successful",
        "user": public_user(user),
    }), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = get_user_by_email(current_app.config["DB_PATH"], email)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": public_user(user),
    }), 200
