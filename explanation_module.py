from gemini_config import client


def explain_topic(topic: str) -> str:
    """
    Explains any educational topic using Gemini.
    """

    prompt = f"""
You are EduGenie, an intelligent AI educational tutor.

Your task is to explain the given topic in a simple, beginner-friendly way.

Respond ONLY in Markdown.

Structure:

# 📘 Title

## 📖 What is it?

Explain the topic in simple language.

## ⚙️ How it Works

Explain step by step.

## 🔑 Key Concepts

- Point 1
- Point 2
- Point 3

## 💡 Example

Give a practical example.

## 🎯 Summary

Provide 3-5 quick revision points.

Topic:

{topic}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

        return "# Error\nNo explanation generated."

    except Exception as e:
        return f"# Error\n\n{e}"
