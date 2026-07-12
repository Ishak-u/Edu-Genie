import json
import re

from gemini_config import client


def clean_json_block(text: str) -> str:
    """
    Removes Markdown code blocks from Gemini responses.
    """

    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    return text.strip()


def generate_quiz(passage: str):
    """
    Generates exactly 3 MCQs from the given educational passage.
    Returns a Python list of dictionaries.
    """

    prompt = f"""
You are EduGenie, an AI Educational Assistant.

Read the passage carefully.

Generate EXACTLY THREE multiple-choice questions.

Rules:

- Return ONLY valid JSON.
- Do NOT write explanations.
- Do NOT use Markdown.
- Each question must contain exactly four options.
- Include the correct answer.

Return in this format:

[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "A"
  }}
]

Passage:

{passage}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            return {
                "success": False,
                "error": "Empty response received from Gemini."
            }

        cleaned = clean_json_block(response.text)

        quiz = json.loads(cleaned)

        return {
            "success": True,
            "quiz": quiz
        }

    except json.JSONDecodeError as e:

        return {
            "success": False,
            "error": "JSON Parsing Failed",
            "details": str(e),
            "raw_response": response.text if "response" in locals() else ""
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }