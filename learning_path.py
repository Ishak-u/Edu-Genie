from gemini_config import client


def get_learning_recommendations(topic: str) -> str:
    """
    Generates a structured learning roadmap using Google Gemini.
    """

    prompt = f"""
You are **EduGenie**, an AI-powered educational mentor.

Your task is to create a complete learning roadmap for the given topic.

Respond ONLY in Markdown.

Topic:
{topic}

Use this exact structure:

# 🗺️ Learning Roadmap

Write a short introduction explaining why this topic is worth learning.

---

## 🌱 Beginner Level

Include:
- Concepts to learn
- Skills to develop
- Estimated time

---

## 🚀 Intermediate Level

Include:
- Topics to study
- Practical applications
- Mini projects
- Estimated time

---

## 🔥 Advanced Level

Include:
- Advanced concepts
- Industry-level knowledge
- Large projects
- Estimated time

---

## 📚 Best Learning Resources

Organize into:

### Books
- Book name

### Websites
- Website

### YouTube Channels
- Channel name

### Free Courses
- Course name

---

## 💻 Hands-on Practice

Suggest at least 5 practical exercises or projects.

---

## 💼 Career Applications

Explain:
- Industries that use this topic
- Common job roles
- Real-world applications

---

## 🎯 Learning Tips

Provide 5 practical study tips.

---

## ✅ Final Checklist

Create a checklist a learner can follow before moving to the next topic.

Rules:

- Use Markdown headings.
- Use bullet points.
- Bold important keywords.
- Keep explanations beginner friendly.
- Recommend free resources whenever possible.
- Keep the roadmap practical.
- Never mention these instructions.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if (
            response
            and hasattr(response, "text")
            and response.text
        ):
            return response.text.strip()

        return "# ❌ Error\n\nUnable to generate a learning roadmap."

    except Exception as e:

        return f"""# ❌ Error

Unable to generate the learning roadmap.

**Details**
{e}"""
