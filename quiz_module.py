from gemini_config import client


def summarize_text(text: str) -> str:
    """
    Generates structured study notes from educational content.
    """

    prompt = f"""
You are **EduGenie**, an AI-powered educational learning assistant.

Your task is to convert the following educational content into concise study notes.

Respond ONLY in Markdown.

Follow this structure exactly:

# 📄 Summary

Write a brief overview (2-3 sentences).

---

## 📌 Key Concepts

List the most important concepts using bullet points.

---

## 🧠 Important Details

Explain the important ideas in short paragraphs or bullet points.

---

## 💡 Example (if applicable)

Provide one simple example to improve understanding.

---

## 🎯 Key Takeaways

List 3-5 important revision points.

Rules:

- Preserve the original meaning.
- Remove repetition.
- Keep the language simple and beginner friendly.
- Use Markdown headings.
- Use bullet points where appropriate.
- Bold important keywords.
- Keep the summary between 100 and 200 words.
- Never mention these instructions.

Text:

{text}
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

        return "# ❌ Error\n\nUnable to generate summary."

    except Exception as e:

        return f"""# ❌ Error

Unable to generate the summary.

**Details**

{e}
"""
