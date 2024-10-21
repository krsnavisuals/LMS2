import sqlite3
from werkzeug.security import generate_password_hash


# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Insert a librarian if no such user exists
    cursor.execute("""
        SELECT COUNT(*) FROM users WHERE role = 'librarian'
    """)
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """,
            ("librarian", generate_password_hash("librarian"), "librarian"),
        )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at timestamp NOT NULL DEFAULT current_timestamp,
            description TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ebooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            date_issued date NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ebook_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ebook_id INTEGER NOT NULL,
            request_date date NOT NULL,
            return_date date NOT NULL,
            status TEXT NOT NULL, -- e.g., 'requested', 'granted', 'returned', 'expired'
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (ebook_id) REFERENCES ebooks(id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ebook_id INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            feedback_date date NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (ebook_id) REFERENCES ebooks(id)
        );
    """)
    conn.commit()
    conn.close()
