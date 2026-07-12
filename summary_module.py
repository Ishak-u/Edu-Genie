from gemini_config import client


def summarize_text(text: str) -> str:
    """
    Generates a concise educational summary from long text.
    """

    prompt = f"""
You are EduGenie, an AI educational assistant.

Summarize the following educational content.

Instructions:
- Keep all important concepts.
- Remove repetition and unnecessary details.
- Use simple, easy-to-understand English.
- Write in short paragraphs or bullet points when appropriate.
- Keep the summary between 100 and 200 words.
- Preserve the original meaning.

Text:

{text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "Unable to generate summary."

    except Exception as e:
        return f"Error generating summary: {str(e)}"