from gemini_config import client


def answer_question(question: str) -> str:
    """
    Answers educational questions using Gemini.
    """

    prompt = f"""
You are EduGenie, an AI educational tutor.

Answer the following question accurately.

Rules:

- Be educational.
- Be beginner friendly.
- Use examples whenever possible.
- Explain step-by-step if required.
- Keep the answer concise but informative.

Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "No answer generated."

    except Exception as e:
        return f"Error: {str(e)}"