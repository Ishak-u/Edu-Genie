
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"

SYSTEM_PROMPT = """
You are Edu-Genie, an educational assistant.

Use the available MCP tools when they help answer the user's request.
- Retrieve educational notes when the user asks about study material.
- Generate a quiz when the user requests practice questions.
- Retrieve learning progress when the user asks about their progress.

Base answers on retrieved information when available.
Be clear, accurate, and student-friendly. Do not invent retrieved notes
or learning-progress records.
"""


async def run_agent(user_input: str) -> str:
    """Run the Edu-Genie agent with the available MCP tools."""
    if not user_input.strip():
        raise ValueError("user_input cannot be empty")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from the .env file.")

    client = MultiServerMCPClient(
        {
            "edu_genie": {
                "transport": "http",
                "url": MCP_SERVER_URL,
            }
        }
    )

    tools = await client.get_tools()

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    final_message = result["messages"][-1]
    content = final_message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and "text" in block
        )

    return str(content)
