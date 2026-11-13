# app/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # All three are required because of the DB schema
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    db = get_db()

    # Check for existing username OR email
    existing = db.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?",
        (username, email),
    ).fetchone()

    if existing is not None:
        return jsonify({"error": "Username or email already taken"}), 400

    password_hash = generate_password_hash(password)

    db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    db.commit()

    return jsonify({"username": username, "email": email}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        # Keep the error generic
        return jsonify({"error": "Invalid credentials"}), 401

    db = get_db()
    user = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()

    # Don't reveal whether username or password was wrong
    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    stored_hash = user["password_hash"]

    if not check_password_hash(stored_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Authenticated for this request only; no token/session yet
    return jsonify({"username": user["username"]}), 200