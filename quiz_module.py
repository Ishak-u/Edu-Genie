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
    """

    prompt = f"""
You are EduGenie, an AI-powered educational tutor.

Generate EXACTLY 3 multiple-choice questions from the passage below.

IMPORTANT RULES

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT include explanations outside the JSON.
- Each question must have exactly four options.
- Options must be labeled A, B, C, D.
- "correct_answer" must contain ONLY A, B, C, or D.
- Questions should test understanding, not memorization.
- Difficulty: Beginner to Intermediate.

JSON FORMAT

[
    {{
        "question":"...",
        "options":{{
            "A":"...",
            "B":"...",
            "C":"...",
            "D":"..."
        }},
        "correct_answer":"A",
        "explanation":"Why option A is correct."
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

        if not response or not response.text:

            return {
                "success": False,
                "error": "Gemini returned an empty response."
            }

        cleaned = clean_json_block(response.text)

        quiz = json.loads(cleaned)

        if not isinstance(quiz, list):

            return {
                "success": False,
                "error": "Quiz format is invalid."
            }

        if len(quiz) != 3:

            return {
                "success": False,
                "error": "Gemini did not generate exactly 3 questions."
            }

        required = {
            "question",
            "options",
            "correct_answer",
            "explanation"
        }

        for q in quiz:

            if not required.issubset(q):

                return {
                    "success": False,
                    "error": "A question is missing required fields."
                }

        return {
            "success": True,
            "quiz": quiz
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "error": "Gemini returned invalid JSON.",
            "raw_response": response.text if "response" in locals() else ""
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
