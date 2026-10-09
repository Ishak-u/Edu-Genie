import time
from functools import wraps
from db.database import log_tool_call
import json
import re

from fastmcp import FastMCP

from db.database import get_progress
from gemini_config import client



def logged_tool(tool_name: str):
    """Decorator that logs a tool's execution and outcome."""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            arguments = {"args": args, "kwargs": kwargs}

            try:
                result = function(*args, **kwargs)
            except Exception as exc:
                log_tool_call(
                    tool_name,
                    arguments,
                    (time.perf_counter() - start) * 1000,
                    False,
                    str(exc),
                )
                raise

            log_tool_call(
                tool_name,
                arguments,
                (time.perf_counter() - start) * 1000,
                True,
            )
            return result

        return wrapper
    return decorator
mcp = FastMCP("Edu-Genie Agent Mesh")


@mcp.tool
@logged_tool("retrieve_notes")
def retrieve_notes(query: str, k: int = 3) -> list[dict]:
    """Retrieve relevant educational notes using SQLite keyword search."""

    if not query.strip():
        raise ValueError("query cannot be empty")

    if not 1 <= k <= 10:
        raise ValueError("k must be between 1 and 10")

    # Import the database path from our shared database module.
    from db.database import get_connection

    terms = [
        term for term in re.findall(r"\w+", query.lower())
        if len(term) > 1
    ]

    if not terms:
        return []

    # Simple MVP keyword search. This is not semantic vector search.
    conditions = " OR ".join(
        "LOWER(content) LIKE ?" for _ in terms
    )
    parameters = [f"%{term}%" for term in terms]

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT id, title, content
            FROM notes
            WHERE {conditions}
            ORDER BY id DESC
            LIMIT ?
            """,
            (*parameters, k),
        ).fetchall()

    return [dict(row) for row in rows]


@mcp.tool
@logged_tool("generate_quiz")
def generate_quiz(
    topic: str,
    difficulty: str = "medium",
    n: int = 5,
) -> list[dict]:
    """Generate multiple-choice questions about a topic using Gemini."""

    if not topic.strip():
        raise ValueError("topic cannot be empty")

    if difficulty.lower() not in {"easy", "medium", "hard"}:
        raise ValueError("difficulty must be easy, medium, or hard")

    if not 1 <= n <= 10:
        raise ValueError("n must be between 1 and 10")

    prompt = f"""
Create {n} multiple-choice quiz questions about: {topic}
Difficulty: {difficulty}

Return ONLY a JSON array. Each item must contain:
- question: string
- options: array of exactly four strings
- answer: exact text of the correct option

Return no Markdown fences or extra commentary.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if not response or not response.text:
        raise RuntimeError("Gemini returned an empty response")

    raw = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response.text.strip(),
        flags=re.IGNORECASE,
    ).strip()

    questions = json.loads(raw)

    if not isinstance(questions, list) or len(questions) != n:
        raise ValueError("Gemini returned an unexpected number of questions")

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Invalid question object")

        if not all(
            key in question for key in ("question", "options", "answer")
        ):
            raise ValueError("Question is missing required fields")

        if (
            not isinstance(question["options"], list)
            or len(question["options"]) != 4
        ):
            raise ValueError("Each question must have four options")

        if question["answer"] not in question["options"]:
            raise ValueError("Correct answer must match one of the options")

    return questions


@mcp.tool
@logged_tool("get_user_progress")
def get_user_progress(user_id: str) -> list[dict]:
    """Retrieve saved learning progress for a user from SQLite."""

    if not user_id.strip():
        raise ValueError("user_id cannot be empty")

    return get_progress(user_id)


if __name__ == "__main__":
    mcp.run()
