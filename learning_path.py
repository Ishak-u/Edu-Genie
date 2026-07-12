from gemini_config import client


def get_learning_recommendations(topic: str) -> str:
    """
    Generates a personalized learning roadmap for a given topic.
    """

    prompt = f"""
You are EduGenie, an intelligent educational learning assistant.

Create a personalized learning path for the following topic.

Topic:
{topic}

Requirements:

1. Beginner Level
   - Fundamental concepts
   - Basic skills

2. Intermediate Level
   - Topics to learn next
   - Practical applications

3. Advanced Level
   - Advanced concepts
   - Industry knowledge

4. Recommended Resources
   - Books
   - Websites
   - YouTube Channels
   - Free Online Courses

5. Practice Ideas
   - Small projects
   - Exercises

6. Career Applications
   - Explain where this topic is used in real life.

Use headings and bullet points.
Keep the response beginner friendly.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text

        return "Unable to generate learning recommendations."

    except Exception as e:
        return f"Error generating learning path: {str(e)}"