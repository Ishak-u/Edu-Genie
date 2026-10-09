import json
import sqlite3
from pathlib import Path

# Store the database in the project root, regardless of the
# directory from which the application is started.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "edu_genie.db"


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with named-column access."""
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the progress and tool-call logging tables."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_progress_user
            ON learning_progress(user_id)
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tool_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                arguments TEXT NOT NULL,
                latency_ms REAL NOT NULL,
                success INTEGER NOT NULL,
                error_message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_progress(user_id: str) -> list[dict]:
    """Return saved learning results for a user."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT topic, score, created_at
            FROM learning_progress
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def log_progress(user_id: str, topic: str, score: float) -> None:
    """Persist a learning result."""
    if not user_id.strip():
        raise ValueError("user_id cannot be empty")

    if not topic.strip():
        raise ValueError("topic cannot be empty")

    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO learning_progress (user_id, topic, score)
            VALUES (?, ?, ?)
            """,
            (user_id, topic, score)
        )

def initialize_notes_table() -> None:
    """Create the educational notes table used by MCP retrieval."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

def log_tool_call(
    tool_name: str,
    arguments: dict,
    latency_ms: float,
    success: bool,
    error_message: str | None = None,
) -> None:
    """Record an MCP tool call and its execution result."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO tool_logs (
                tool_name,
                arguments,
                latency_ms,
                success,
                error_message
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                tool_name,
                json.dumps(arguments),
                max(0.0, latency_ms),
                int(success),
                error_message,
            ),
        )
