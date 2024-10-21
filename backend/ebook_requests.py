from flask_jwt_extended import get_jwt_identity, jwt_required
from db import get_db_connection
from flask import Blueprint, request, jsonify
from datetime import datetime
from cache import cache
from users import UserIdentity, is_user

ebook_requests_bp = Blueprint("ebook_requests", __name__)


@ebook_requests_bp.route("/ebook_requests", methods=["POST"])
@jwt_required()
def create_ebook_request():
    current_user = get_jwt_identity()

    if not is_user(current_user):
        return jsonify({"message": "You are not a user"}), 403

    new_request = request.get_json()
    user_id = new_request.get("user_id")
    ebook_id = new_request.get("ebook_id")
    request_date = datetime.now().date()
    return_date = datetime.fromisoformat(new_request.get("return_date")).date()
    status = "requested"

    if not user_id or not ebook_id or not return_date:
        return jsonify(
            {"message": "User ID, Ebook ID, and Return Date are required!"}
        ), 400

    if return_date < request_date:
        return jsonify(
            {"message": "Return Date cannot be earlier than Request Date!"}
        ), 400

    # Check the number of existing requests by the user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM ebook_requests
        WHERE user_id = ? AND status = 'requested'
    """,
        (user_id,),
    )
    request_count = cursor.fetchone()[0]

    if request_count >= 5:
        conn.close()
        return jsonify({"message": "You can only request a maximum of 5 books!"}), 400

    # Create the new ebook request
    cursor.execute(
        """
        INSERT INTO ebook_requests (user_id, ebook_id, request_date, return_date, status)
        VALUES (?, ?, ?, ?, ?)
    """,
        (user_id, ebook_id, request_date.isoformat(), return_date.isoformat(), status),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for all ebooks
    cache.delete("ebooks")

    return jsonify({"message": "Ebook request created successfully!"}), 201


# Get all ebook requests
@ebook_requests_bp.route("/ebook_requests", methods=["GET"])
def get_ebook_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ebook_requests")
    ebook_requests = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in ebook_requests]), 200


# Get all ebook requests by user
@ebook_requests_bp.route("/ebook_requests_user", methods=["GET"])
@jwt_required()
def get_ebook_requests_from_user():
    current_user: UserIdentity = get_jwt_identity()

    if not is_user(current_user):
        return jsonify({"message": "You are not a user"}), 403
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM ebook_requests WHERE user_id = ?", (str(current_user["id"]))
    )
    ebook_requests = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in ebook_requests]), 200


# Get a single ebook request by ID
@ebook_requests_bp.route("/ebook_requests/<int:id>", methods=["GET"])
def get_ebook_request(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ebook_requests WHERE id = ?", (id,))
    ebook_request = cursor.fetchone()
    conn.close()

    if ebook_request is None:
        return jsonify({"message": "Ebook request not found!"}), 404

    return jsonify(dict(ebook_request)), 200


# Update an ebook request
@ebook_requests_bp.route("/ebook_requests/<int:id>", methods=["PUT"])
def update_ebook_request(id):
    update_data = request.get_json()
    status = update_data.get("status")

    if not status:
        return jsonify({"message": "Status is required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE ebook_requests
        SET status = ?
        WHERE id = ?
    """,
        (status, id),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for all ebooks
    cache.delete("ebooks")

    return jsonify({"message": "Ebook request updated successfully!"}), 200


# Delete an ebook request
@ebook_requests_bp.route("/ebook_requests/<int:id>", methods=["DELETE"])
def delete_ebook_request(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ebook_requests WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Invalidate the cache for all ebooks
    cache.delete("ebooks")

    return jsonify({"message": "Ebook request deleted successfully!"}), 200
