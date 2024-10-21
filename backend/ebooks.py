from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection
from cache import cache
from sections import section_exists
from users import UserIdentity, is_librarian, is_user

ebooks_bp = Blueprint("ebooks", __name__)


# Helper function to check if an ebook exists by ID
def ebook_exists(ebook_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ebooks WHERE id = ?", (ebook_id,))
    ebook = cursor.fetchone()
    conn.close()
    return ebook is not None


# Create a new ebook
@ebooks_bp.route("/ebooks", methods=["POST"])
@jwt_required()
def create_ebook():
    current_user: UserIdentity = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 403

    new_ebook = request.get_json()

    # Validate required fields
    if (
        not new_ebook
        or not new_ebook.get("section_id")
        or not new_ebook.get("name")
        or not new_ebook.get("content")
        or not new_ebook.get("author")
        or not new_ebook.get("date_issued")
    ):
        return jsonify(
            {
                "message": "section_id, name, content, author, and date_issued are required!"
            }
        ), 400

    section_id = new_ebook["section_id"]

    # Validate section existence
    if not section_exists(section_id):
        return jsonify({"message": "Section not found!"}), 404

    name = new_ebook["name"]
    content = new_ebook["content"]
    author = new_ebook["author"]
    date_issued = new_ebook["date_issued"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO ebooks (section_id, name, content, author, date_issued)
        VALUES (?, ?, ?, ?, ?)
        """,
        (section_id, name, content, author, date_issued),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for all ebooks
    cache.delete("ebooks")
    cache.delete("sections")

    return jsonify({"message": "Ebook created successfully!"}), 201


# Get all ebooks
@ebooks_bp.route("/ebooks", methods=["GET"])
@cache.cached(timeout=60, key_prefix="ebooks")
def get_ebooks():
    section_id = request.args.get("section_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    # # if section_id:
    #     cursor.execute("SELECT * FROM ebooks WHERE section_id = ?", (section_id,))
    # else:
    cursor.execute("SELECT * FROM ebooks")

    ebooks = cursor.fetchall()
    conn.close()

    ebooks_list = [dict(ebook) for ebook in ebooks]

    return jsonify(ebooks_list)


# Get an ebook by ID
@ebooks_bp.route("/ebooks/<int:id>", methods=["GET"])
def get_ebook(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ebooks WHERE id = ?", (id,))
    ebook = cursor.fetchone()
    conn.close()

    if ebook is None:
        return jsonify({"message": "Ebook not found!"}), 404

    return jsonify(dict(ebook))


# Update an ebook
@ebooks_bp.route("/ebooks/<int:id>", methods=["PUT"])
@jwt_required()
def update_ebook(id):
    current_user = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 403

    # Check if the ebook exists
    if not ebook_exists(id):
        return jsonify({"message": "Ebook not found!"}), 404

    updated_ebook = request.get_json()

    # Validate required fields
    if (
        not updated_ebook
        or not updated_ebook.get("name")
        or not updated_ebook.get("content")
        or not updated_ebook.get("author")
        or not updated_ebook.get("date_issued")
    ):
        return jsonify(
            {"message": "name, content, author, and date_issued are required!"}
        ), 400

    name = updated_ebook["name"]
    content = updated_ebook["content"]
    author = updated_ebook["author"]
    date_issued = updated_ebook["date_issued"]
    section_id = updated_ebook["section_id"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE ebooks
        SET name = ?, content = ?, author = ?, date_issued = ?, section_id = ?
        WHERE id = ?
        """,
        (name, content, author, date_issued, section_id, id),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for the updated ebook
    cache.delete("ebooks")
    cache.delete("sections")

    return jsonify({"message": "Ebook updated successfully!"})


# Delete an ebook
@ebooks_bp.route("/ebooks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_ebook(id):
    current_user = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 403

    # Check if the ebook exists
    if not ebook_exists(id):
        return jsonify({"message": "Ebook not found!"}), 404

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ebooks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Invalidate the cache for the deleted ebook
    cache.delete("ebooks")
    cache.delete("sections")

    return jsonify({"message": "Ebook deleted successfully!"})


# Get all ebooks that have been requested by a specific user
@ebooks_bp.route("/ebooks/requests", methods=["GET"])
@jwt_required()
def get_ebooks_requested_by_user():
    current_user: UserIdentity = get_jwt_identity()

    if not is_user(current_user):
        return jsonify({"message": "You are not a user"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM EBOOKS
        """
    )
    ebooks = cursor.fetchall()
    ebooks = [dict(ebook) for ebook in ebooks]

    for ebook in ebooks:
        cursor.execute(
            """
            SELECT status FROM ebook_requests
            WHERE user_id = ? AND ebook_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (current_user["id"], ebook["id"]),
        )

        status = cursor.fetchone()
        ebook["status"] = status[0] if status else None

    conn.close()

    return jsonify(ebooks)


# Get all ebooks that have been given feedback by a specific user
@ebooks_bp.route("/ebooks/feedback/<int:user_id>", methods=["GET"])
def get_ebooks_feedback_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT ebooks.*
        FROM ebooks
        JOIN feedback ON ebooks.id = feedback.ebook_id
        WHERE feedback.user_id = ?
    """,
        (user_id,),
    )
    ebooks = cursor.fetchall()
    conn.close()

    ebooks_list = [dict(ebook) for ebook in ebooks]
    return jsonify(ebooks_list)
