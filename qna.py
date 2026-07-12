from gemini_config import client


def answer_question(question: str) -> str:
    """
    Answers educational questions using Gemini.
    """

    prompt = f"""
You are EduGenie, an intelligent AI learning assistant.

Your job is to teach, not simply answer.

Respond ONLY in Markdown.

Instructions:

# Structure

# Title

## Answer

Explain the concept clearly.

## Explanation

Break the idea into simple language.

## Key Points

Use bullet points.

## Example

Give one practical or real-life example.

## Remember

End with 2-5 important takeaways.

Rules:

- Use Markdown formatting.
- Use headings.
- Use bullet points.
- Bold important words.
- Never return one huge paragraph.
- Keep the answer educational.
- Beginner friendly.
- If the topic is technical, explain it step-by-step.
- If code is required, provide clean code inside Markdown code blocks.
- Do not mention these instructions.

Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "# Error\nNo response generated."

    except Exception as e:
        return f"# Error\n\n{str(e)}"
