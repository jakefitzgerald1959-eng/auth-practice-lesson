from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from sqlite3 import IntegrityError

from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/")


@bp.post("register")
def register():
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    # Basic validation
    errors = {}
    if not username:
        errors["username"] = "Username is required."
    if not email:
        errors["email"] = "Email is required."
    if not password:
        errors["password"] = "Password is required."

    if errors:
        return jsonify({"errors": errors}), 400

    password_hash = generate_password_hash(password)

    db = get_db()
    try:
        db.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash),
        )
        db.commit()
    except IntegrityError:
        # username or email already exists
        return (
            jsonify(
                {
                    "error": "Username or email already exists.",
                    "username": username,
                    "email": email,
                }
            ),
            409,
        )

    # Success: don't return password or hash
    return (
        jsonify(
            {
                "username": username,
                "email": email,
            }
        ),
        201,
    )