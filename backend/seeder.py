from db import get_db_connection, init_db
from datetime import datetime

def seed_sections():
    # Connect to the SQLite database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Dummy data to insert
    dummy_data = [
        ("Science Fiction", "Books that explore imaginative and futuristic concepts such as advanced science, technology, space exploration, time travel, parallel universes, etc."),
        ("Fantasy", "Books that contain magical or supernatural elements that do not exist in the real world."),
        ("Mystery", "Books that involve solving a crime or uncovering secrets."),
        ("Non-Fiction", "Books that provide factual information about real events, people, and places."),
        ("Biography", "Books that provide an account of a person's life."),
    ]

    # Insert dummy data into the sections table
    for name, description in dummy_data:
        cursor.execute(
            """
            INSERT INTO sections (name, description, created_at)
            VALUES (?, ?, ?)
            """,
            (name, description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Sections data inserted successfully!")

def seed_ebooks():
    # Connect to the SQLite database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Dummy data to insert
    dummy_ebooks = [
        (1, "Dune", "A science fiction novel by Frank Herbert.", "Frank Herbert", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, "Harry Potter and the Sorcerer's Stone", "A fantasy novel by J.K. Rowling.", "J.K. Rowling", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, "The Hound of the Baskervilles", "A mystery novel by Arthur Conan Doyle.", "Arthur Conan Doyle", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, "Sapiens: A Brief History of Humankind", "A non-fiction book by Yuval Noah Harari.", "Yuval Noah Harari", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, "The Diary of a Young Girl", "A biography by Anne Frank.", "Anne Frank", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, "Neuromancer", "A science fiction novel by William Gibson.", "William Gibson", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, "The Hobbit", "A fantasy novel by J.R.R. Tolkien.", "J.R.R. Tolkien", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, "Gone Girl", "A mystery novel by Gillian Flynn.", "Gillian Flynn", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, "Educated", "A non-fiction book by Tara Westover.", "Tara Westover", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, "Steve Jobs", "A biography by Walter Isaacson.", "Walter Isaacson", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, "Foundation", "A science fiction novel by Isaac Asimov.", "Isaac Asimov", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, "The Name of the Wind", "A fantasy novel by Patrick Rothfuss.", "Patrick Rothfuss", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, "The Girl with the Dragon Tattoo", "A mystery novel by Stieg Larsson.", "Stieg Larsson", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, "The Immortal Life of Henrietta Lacks", "A non-fiction book by Rebecca Skloot.", "Rebecca Skloot", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, "The Wright Brothers", "A biography by David McCullough.", "David McCullough", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, "Snow Crash", "A science fiction novel by Neal Stephenson.", "Neal Stephenson", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, "American Gods", "A fantasy novel by Neil Gaiman.", "Neil Gaiman", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, "Big Little Lies", "A mystery novel by Liane Moriarty.", "Liane Moriarty", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, "Unbroken", "A non-fiction book by Laura Hillenbrand.", "Laura Hillenbrand", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, "Alexander Hamilton", "A biography by Ron Chernow.", "Ron Chernow", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1, "Hyperion", "A science fiction novel by Dan Simmons.", "Dan Simmons", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, "The Way of Kings", "A fantasy novel by Brandon Sanderson.", "Brandon Sanderson", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, "In the Woods", "A mystery novel by Tana French.", "Tana French", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4, "The Glass Castle", "A non-fiction book by Jeannette Walls.", "Jeannette Walls", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5, "The Autobiography of Malcolm X", "A biography by Malcolm X and Alex Haley.", "Malcolm X and Alex Haley", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]

    # Insert dummy data into the ebooks table
    for section_id, name, content, author, date_issued in dummy_ebooks:
        cursor.execute(
            """
            INSERT INTO ebooks (section_id, name, content, author, date_issued)
            VALUES (?, ?, ?, ?, ?)
            """,
            (section_id, name, content, author, date_issued)
        )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Ebooks data inserted successfully!")

# Call the functions to seed the database
if __name__ == "__main__":
    init_db()
    seed_sections()
    seed_ebooks()
    print("All dummy data inserted successfully!")
