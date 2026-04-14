# Python Tutor Chatbot (FastAPI)

This repository contains a simple Python tutor chatbot using a Google Gemini LLM via LangChain, and a FastAPI wrapper to expose a `/chat` endpoint.

Quick start

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key to `.env`:

```
GOOGLE_API_KEY=your_api_key_here
```

4. Run the API server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8085
```

5. Call the API:

```bash
curl -X POST "http://localhost:8085/chat" -H "Content-Type: application/json" -d '{"message":"How do I write a for loop in Python?"}'
```

Notes

- The service uses the functions in `agent_demo.py` (`create_llm`, `create_prompt`, `send_message`, and `SimpleMemory`).
- Responses are truncated to 500 characters and the LLM is configured to produce shorter outputs. Adjust `max_output_tokens` or truncation length as needed.
