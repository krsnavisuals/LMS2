from typing import TypedDict
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_db_connection


users_bp = Blueprint("auth", __name__)

class UserIdentity(TypedDict):
    id: int
    username: str
    role: str

def is_librarian(user: UserIdentity) -> bool:
    return user['role'] == 'librarian'

def is_user(user: UserIdentity) -> bool:
    return user['role'] == 'user'

@users_bp.route("/get-users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE role = ?", ("user",))
    users = cursor.fetchall()
    conn.close()

    users_list = []
    for user in users:
        users_list.append({
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        })

    return jsonify(users_list), 200


# User registration
@users_bp.route("/register-user", methods=["POST"])
def register():
    new_user = request.get_json()
    username = new_user.get("username")
    password = new_user.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Username already exists!"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """,
        (username, hashed_password, "user"),
    )
    conn.commit()
    conn.close()

    access_token = create_access_token(
        identity={"id": user["id"], "username": user["username"], "role": user["role"]},
        expires_delta=False
    )
    return jsonify(
        {
            "message": "Register successful!",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            },
            "token": access_token,
        }
    ), 200


# User login
@users_bp.route("/login-user", methods=["POST"])
def login():
    login_details = request.get_json()
    username = login_details.get("username")
    password = login_details.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password!"}), 401

    if user["role"] != "user":
        return jsonify({"message": "You are not a user!"}), 401

    access_token = create_access_token(
        identity={"id": user["id"], "username": user["username"], "role": user["role"]},
        expires_delta=False
    )
    return jsonify(
        {
            "message": "Login successful!",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            },
            "token": access_token,
        }
    ), 200


# Librarian login
@users_bp.route("/login-librarian", methods=["POST"])
def librarian_login():
    login_details = request.get_json()
    username = login_details.get("username")
    password = login_details.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid username or password"}), 401

    if user["role"] != "librarian":
        return jsonify({"message": "You are not a librarian!"}), 401

    access_token = create_access_token(
        identity={"id": user["id"], "username": user["username"], "role": user["role"]},
        expires_delta=False
    )
    return jsonify(
        {
            "message": "Librarian login successful!",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            },
            "token": access_token,
        }
    ), 200


# Protected route example
@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user: UserIdentity = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
