
from gemini_config import client
import json
import re


def generate_quiz(text: str):
    """
    Generates a multiple-choice quiz from educational content.
    Returns a list of questions with options and correct answers.
    """

    if not text or not text.strip():
        return {"error": "Please provide educational content to generate a quiz."}

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create 5 multiple-choice questions based only on the educational content below.

Return ONLY a valid JSON array. Do not use Markdown fences.

Each array item must follow this structure:
{{
  "question": "Question text",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Exact text of the correct option"
}}

Rules:
- Each question must have exactly four options.
- Only one option should be correct.
- Questions should test understanding, not just memorization.
- Use only facts supported by the supplied content.

Educational content:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return {"error": "Unable to generate a quiz."}

        result = response.text.strip()

        # Handle a response wrapped in Markdown code fences.
        result = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            result,
            flags=re.IGNORECASE
        ).strip()

        questions = json.loads(result)

        if not isinstance(questions, list) or not questions:
            return {"error": "The AI returned an invalid quiz format."}

        # Validate the structure before returning it.
        for question in questions:
            if not isinstance(question, dict):
                return {"error": "The AI returned an invalid question."}

            if not all(key in question for key in ("question", "options", "answer")):
                return {"error": "A generated question is missing required fields."}

            if not isinstance(question["options"], list) or len(question["options"]) != 4:
                return {"error": "A generated question does not have four options."}

            if question["answer"] not in question["options"]:
                return {"error": "A correct answer does not match any option."}

        return questions

    except json.JSONDecodeError:
        return {"error": "The AI returned invalid JSON. Please try again."}

    except Exception:
        return {"error": "Quiz generation failed. Check your Gemini configuration and try again."}
