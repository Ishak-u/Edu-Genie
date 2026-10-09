
from db.database import get_connection, initialize_notes_table

initialize_notes_table()

sample_notes = [
    (
        "Python Variables",
        "Variables store values in Python. A variable can refer to integers, strings, lists, and other objects.",
    ),
    (
        "Python Functions",
        "Functions are reusable blocks of code defined with def. Parameters receive input, and return sends a result back.",
    ),
    (
        "Machine Learning",
        "Machine learning systems learn patterns from data to make predictions or decisions.",
    ),
]

with get_connection() as connection:
    for title, content in sample_notes:
        connection.execute(
            "INSERT INTO notes (title, content) "
            "SELECT ?, ? WHERE NOT EXISTS "
            "(SELECT 1 FROM notes WHERE title = ?)",
            (title, content, title),
        )

print("Sample notes are ready.")
