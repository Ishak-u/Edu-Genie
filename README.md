# Edu-Genie — AI Learning Assistant & Agent Mesh

Edu-Genie is an AI-powered learning platform that helps students understand concepts, ask academic questions, generate quizzes, summarize study material, and discover personalized learning paths.

The **Agent Mesh MVP** extends the existing application with a tool-using AI agent built using LangGraph, FastMCP, Google Gemini, and SQLite. The agent can retrieve saved study notes, generate quizzes, and retrieve learning-progress records through MCP tools.

## Features

### Existing Learning Assistant

* AI-powered concept explanations
* Academic question answering
* Text summarization
* Quiz generation
* Personalized learning-path recommendations
* Web interface built with HTML, CSS, and JavaScript

### Agent Mesh MVP

* **Study-note retrieval:** Search saved educational notes in SQLite.
* **Quiz generation:** Generate multiple-choice questions using Gemini.
* **Progress retrieval:** Retrieve a user's saved learning scores.
* **Tool-using AI agent:** LangGraph agent connects to MCP tools.
* **FastAPI integration:** Exposes the agent through `POST /agent`.
* **Tool-call logging:** Records tool name, execution time, success status, and errors in SQLite.

## Tech Stack

| Component                 | Technology               |
| ------------------------- | ------------------------ |
| Frontend                  | HTML, CSS, JavaScript    |
| API                       | FastAPI                  |
| Agent orchestration       | LangGraph                |
| Tool protocol/server      | FastMCP                  |
| Language model            | Google Gemini API        |
| Database                  | SQLite                   |
| MCP client                | `langchain-mcp-adapters` |
| Environment configuration | `python-dotenv`          |

## Project Structure

```text
Edu-Genie/
├── main.py
├── gemini_config.py
├── explanation_module.py
├── qna.py
├── summary_module.py
├── quiz_module.py
├── learning_path.py
├── requirements.txt
├── README.md
├── agent/
│   ├── __init__.py
│   └── graph.py
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   └── http_server.py
├── db/
│   ├── __init__.py
│   └── database.py
├── tests/
│   ├── __init__.py
│   └── seed_notes.py
├── templates/
├── static/
├── .env
└── edu_genie.db
```

The database file is created locally. Do not commit `.env` or a database containing private user data.

## Setup

### 1. Create and activate an environment

Use your preferred Python environment manager. For Conda:

```powershell
conda create -n edugenie python=3.11 -y
conda activate edugenie
```

If you already have a working `edugenie` environment, you do not need to recreate it.

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

Check for dependency conflicts:

```powershell
python -m pip check
```

### 3. Configure Gemini

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own key. Never commit the actual API key to source control.

### 4. Initialize and seed sample notes

Initialize the database using the project's database setup functions, then run:

```powershell
python -m tests.seed_notes
```

This adds sample educational notes for testing retrieval.

## Run the Application

Open two terminals in the project root and activate the same environment in each.

**Terminal 1 — Start the MCP HTTP server**

```powershell
python -m mcp_server.http_server
```

The MCP server listens at:

```text
http://127.0.0.1:8001/mcp
```

**Terminal 2 — Start the FastAPI application**

```powershell
uvicorn main:app --reload
```

Open the existing web application at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Test the Agent Endpoint

With both servers running, execute:

```powershell
python -c "from fastapi.testclient import TestClient; from main import app; c=TestClient(app); r=c.post('/agent', data={'message':'Explain Python functions using my saved study notes.'}); print('Status:', r.status_code); print(r.json())"
```

A successful request returns HTTP `200` and a JSON response containing the original message and the agent's answer.

### Available MCP tools

| Tool                | Purpose                                      |
| ------------------- | -------------------------------------------- |
| `retrieve_notes`    | Search saved notes by keywords               |
| `generate_quiz`     | Generate validated multiple-choice questions |
| `get_user_progress` | Retrieve learning records for a user         |

Tool execution records are stored in the SQLite `tool_logs` table.

## How the Agent Mesh Works

1. A user sends a message to the FastAPI `/agent` endpoint.
2. The LangGraph agent interprets the request.
3. The agent selects an available MCP tool when needed.
4. The MCP client communicates with the FastMCP server.
5. The tool accesses saved notes, learning progress, or Gemini quiz generation.
6. The agent uses the tool result to formulate its final response.
7. Tool execution details are logged in SQLite.

## Security Notes

* Store API keys in `.env` and exclude the file from Git.
* Do not expose the local MCP server publicly without appropriate authentication and access controls.
* Add authentication and authorization before exposing user-specific learning records to multiple users.
* Avoid logging sensitive user data or API keys.

## Roadmap

Potential future improvements include document ingestion and retrieval-augmented generation (RAG), source-grounded tutoring, persistent conversational memory, automated integration tests, and user authentication.

## License

This project is licensed under the MIT License, subject to the terms of the repository's `LICENSE` file.

## Author

**Ishak Baba Shaik**
