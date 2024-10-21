from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from db import get_db_connection
from users import UserIdentity, is_librarian, is_user

stats_bp = Blueprint("stats", __name__)

# Function to retrieve statistics for the librarian (admin)
@stats_bp.route('/stats/librarian', methods=['GET'])
@jwt_required()
def librarian_stats():    
    current_user: UserIdentity = get_jwt_identity()

    if not is_librarian(current_user):
        return jsonify({"message": "You are not a librarian"}), 403
    
    print(f"{current_user=}")
    
    conn = get_db_connection()

    # Total Number of Ebooks
    total_ebooks = conn.execute('SELECT COUNT(*) FROM ebooks').fetchone()['COUNT(*)']

    # Total Number of Sections
    total_sections = conn.execute('SELECT COUNT(*) FROM sections').fetchone()['COUNT(*)']

    # Ebook Activity
    ebook_activity = conn.execute('''
        SELECT ebooks.name, 
               COUNT(ebook_requests.id) AS request_count 
        FROM ebooks 
        LEFT JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        GROUP BY ebooks.name
    ''').fetchall()

    # Top Borrowed Ebooks
    top_borrowed_ebooks = conn.execute('''
        SELECT ebooks.name, 
               COUNT(ebook_requests.id) AS borrow_count 
        FROM ebooks 
        LEFT JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        GROUP BY ebooks.name 
        ORDER BY borrow_count DESC 
        LIMIT 5
    ''').fetchall()

    # Active Ebook Requests
    active_requests = conn.execute('''
        SELECT * FROM ebook_requests WHERE status = "granted"
    ''').fetchall()

    # Overdue Ebook Requests
    overdue_requests = conn.execute('''
        SELECT * FROM ebook_requests 
        WHERE status = "granted" AND return_date < DATE('now')
    ''').fetchall()

    # User Activity
    user_activity = conn.execute('''
        SELECT users.username, 
               COUNT(ebook_requests.id) AS total_requests, 
               SUM(CASE WHEN ebook_requests.status = 'granted' THEN 1 ELSE 0 END) AS granted_requests 
        FROM users 
        LEFT JOIN ebook_requests ON users.id = ebook_requests.user_id 
        GROUP BY users.username
    ''').fetchall()

    # Feedback Overview
    feedback_overview = conn.execute('''
        SELECT ebooks.name, 
               COUNT(feedback.id) AS feedback_count, 
               MAX(feedback.feedback_date) AS last_feedback_date 
        FROM feedback 
        LEFT JOIN ebooks ON feedback.ebook_id = ebooks.id 
        GROUP BY ebooks.name
    ''').fetchall()

    # Ebooks by Section
    ebooks_by_section = conn.execute('''
        SELECT sections.name AS section_name, 
               COUNT(ebooks.id) AS ebook_count 
        FROM sections 
        LEFT JOIN ebooks ON sections.id = ebooks.section_id 
        GROUP BY sections.name
    ''').fetchall()

    conn.close()

    return jsonify({
        'total_ebooks': total_ebooks,
        'total_sections': total_sections,
        'ebook_activity': [dict(row) for row in ebook_activity],
        'top_borrowed_ebooks': [dict(row) for row in top_borrowed_ebooks],
        'active_requests': [dict(row) for row in active_requests],
        'overdue_requests': [dict(row) for row in overdue_requests],
        'user_activity': [dict(row) for row in user_activity],
        'feedback_overview': [dict(row) for row in feedback_overview],
        'ebooks_by_section': [dict(row) for row in ebooks_by_section]
    })

# Function to retrieve statistics for the user
@stats_bp.route('/stats/user', methods=['GET'])
@jwt_required()
def user_stats():
    current_user: UserIdentity = get_jwt_identity()

    if not is_user(current_user):
        return jsonify({"message": "You are not a user"}), 403
    
    user_id = current_user['id']
    
    conn = get_db_connection()

    # Borrowing History
    borrowing_history = conn.execute('''
        SELECT ebooks.name, 
               ebook_requests.request_date, 
               ebook_requests.return_date 
        FROM ebooks 
        JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        WHERE ebook_requests.user_id = ? 
    ''', (user_id,)).fetchall()

    # Current Active Requests
    active_requests = conn.execute('''
        SELECT ebooks.name, 
               ebook_requests.request_date, 
               ebook_requests.return_date 
        FROM ebooks 
        JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        WHERE ebook_requests.user_id = ? AND ebook_requests.status = "granted"
    ''', (user_id,)).fetchall()

    # Overdue Books
    overdue_books = conn.execute('''
        SELECT ebooks.name, 
               ebook_requests.return_date 
        FROM ebooks 
        JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        WHERE ebook_requests.user_id = ? AND ebook_requests.status = "granted" AND ebook_requests.return_date < DATE('now')
    ''', (user_id,)).fetchall()

    # Feedback Given
    feedback_given = conn.execute('''
        SELECT ebooks.name, 
               feedback.feedback, 
               feedback.feedback_date 
        FROM ebooks 
        JOIN feedback ON ebooks.id = feedback.ebook_id 
        WHERE feedback.user_id = ? 
    ''', (user_id,)).fetchall()

    # Top Requested Ebooks
    top_requested_ebooks = conn.execute('''
        SELECT ebooks.name, 
               COUNT(ebook_requests.id) AS request_count 
        FROM ebooks 
        LEFT JOIN ebook_requests ON ebooks.id = ebook_requests.ebook_id 
        GROUP BY ebooks.name 
        ORDER BY request_count DESC 
        LIMIT 5
    ''').fetchall()

    # Recently Added Ebooks
    recently_added_ebooks = conn.execute('''
        SELECT name, author, date_issued 
        FROM ebooks 
        ORDER BY date_issued DESC 
        LIMIT 5
    ''').fetchall()

    conn.close()

    return jsonify({
        'borrowing_history': [dict(row) for row in borrowing_history],
        'active_requests': [dict(row) for row in active_requests],
        'overdue_books': [dict(row) for row in overdue_books],
        'feedback_given': [dict(row) for row in feedback_given],
        'top_requested_ebooks': [dict(row) for row in top_requested_ebooks],
        'recently_added_ebooks': [dict(row) for row in recently_added_ebooks]
    })

