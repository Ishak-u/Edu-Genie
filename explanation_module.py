from gemini_config import client


def explain_topic(topic: str) -> str:
    """
    Generates a beginner-friendly explanation for any educational topic.
    """

    prompt = f"""
You are EduGenie, an intelligent educational assistant.

Your task is to explain concepts in a simple, beginner-friendly manner.

Instructions:
- Use easy English.
- Assume the learner has no prior knowledge.
- Keep the explanation between 150-250 words.
- Use short paragraphs.
- Include one real-life example.
- Avoid unnecessary technical jargon.
- End with one interesting fact.

Topic:
{topic}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "Unable to generate explanation."

    except Exception as e:
        return f"Error generating explanation: {str(e)}"