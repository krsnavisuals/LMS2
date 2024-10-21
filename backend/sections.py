from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection
from cache import cache
from users import is_librarian

sections_bp = Blueprint("sections", __name__)


# Helper function to check if a section exists by ID
def section_exists(section_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sections WHERE id = ?", (section_id,))
    section = cursor.fetchone()
    conn.close()
    return section is not None


# Create a new section
@sections_bp.route("/sections", methods=["POST"])
@jwt_required()
def create_section():
    current_user = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 400

    new_section = request.get_json()

    # Validate required fields
    if not new_section or not new_section.get("name") or not new_section.get("description"):
        return jsonify({"message": "Name and description are required!"}), 400

    name = new_section["name"]
    description = new_section["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sections (name, description)
        VALUES (?, ?)
        """,
        (name, description),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for all sections
    cache.delete("sections")

    return jsonify({"message": "Section created successfully!"}), 201


# Get all sections
@sections_bp.route("/sections", methods=["GET"])
@cache.cached(timeout=60, key_prefix="sections")
def get_sections():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sections")
    sections = cursor.fetchall()
    conn.close()

    sections_list = [dict(section) for section in sections]
    return jsonify(sections_list)


# Get a section by ID
@sections_bp.route("/sections/<int:id>", methods=["GET"])
def get_section(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sections WHERE id = ?", (id,))
    section = cursor.fetchone()
    conn.close()

    if section is None:
        return jsonify({"message": "Section not found!"}), 404

    return jsonify(dict(section))


# Update a section
@sections_bp.route("/sections/<int:id>", methods=["PUT"])
@jwt_required()
def update_section(id):
    current_user = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 400

    # Check if the section exists
    if not section_exists(id):
        return jsonify({"message": "Section not found!"}), 404

    updated_section = request.get_json()

    # Validate required fields
    if not updated_section or not updated_section.get("name") or not updated_section.get("description"):
        return jsonify({"message": "Name and description are required!"}), 400

    name = updated_section["name"]
    description = updated_section["description"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE sections
        SET name = ?, description = ?
        WHERE id = ?
        """,
        (name, description, id),
    )
    conn.commit()
    conn.close()

    # Invalidate the cache for the updated section
    cache.delete("sections")

    return jsonify({"message": "Section updated successfully!"})


# Delete a section
@sections_bp.route("/sections/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_section(id):
    current_user = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 400

    # Check if the section exists
    if not section_exists(id):
        return jsonify({"message": "Section not found!"}), 404

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sections WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    # Invalidate the cache for the deleted section
    cache.delete("sections")

    return jsonify({"message": "Section deleted successfully!"})
