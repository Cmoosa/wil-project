import jwt
from datetime import datetime, timedelta
from typing import Dict
from ..config import Config

JWT_ALGORITHM = "HS256"
JWT_EXPIRY_MINUTES = 60 * 8 

def generate_token(user: Dict) -> str:
    """
    Generate a signed JWT for an authenticated user.
    """
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "role": user.get("role", "user"),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES),
    }

    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token

def decode_token(token: str) -> Dict:
    """
    Decode and validate a JWT.
    Raises jwt exceptions if invalid or expired.
    """
    return jwt.decode(
        token,
        Config.SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )
