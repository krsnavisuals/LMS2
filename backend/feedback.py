from db import get_db_connection
from flask import Blueprint, request, jsonify
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

# Create a new feedback entry
@feedback_bp.route('/feedback', methods=['POST'])
def create_feedback():
    new_feedback = request.get_json()
    user_id = new_feedback.get('user_id')
    ebook_id = new_feedback.get('ebook_id')
    feedback_text = new_feedback.get('feedback')
    feedback_date = new_feedback.get('feedback_date', datetime.now().isoformat())

    if not user_id or not ebook_id or not feedback_text:
        return jsonify({'message': 'User ID, Ebook ID, and Feedback are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (user_id, ebook_id, feedback, feedback_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, ebook_id, feedback_text, feedback_date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Feedback created successfully!'}), 201

# Get all feedback entries
@feedback_bp.route('/feedback', methods=['GET'])
def get_feedback():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedback_entries = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in feedback_entries]), 200

# Get a single feedback entry by ID
@feedback_bp.route('/feedback/<int:id>', methods=['GET'])
def get_feedback_entry(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback WHERE id = ?", (id, ))
    feedback_entry = cursor.fetchone()
    conn.close()

    if feedback_entry is None:
        return jsonify({'message': 'Feedback not found!'}), 404

    return jsonify(dict(feedback_entry)), 200

# Update a feedback entry
@feedback_bp.route('/feedback/<int:id>', methods=['PUT'])
def update_feedback(id):
    update_data = request.get_json()
    feedback_text = update_data.get('feedback')

    if not feedback_text:
        return jsonify({'message': 'Feedback is required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE feedback
        SET feedback = ?
        WHERE id = ?
    """, (feedback_text, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Feedback updated successfully!'}), 200

# Delete a feedback entry
@feedback_bp.route('/feedback/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Feedback deleted successfully!'}), 200
