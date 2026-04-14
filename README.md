# LangChain Playground - Python Tutor Chatbot

A modern FastAPI-based Python tutor chatbot using Google's Gemini LLM via LangChain with persistent SQLite conversation memory management.

## 🎯 Features

- **FastAPI REST API** - Clean, modern API with automatic documentation
- **Google Gemini Integration** - Powered by latest Google AI models via LangChain
- **Multi-User Support** - Conversation memory per user with SQLite persistence
- **Type Safety** - Full Pydantic validation for requests/responses
- **Environment Configuration** - Flexible setup via environment variables
- **Clean Architecture** - Modular structure for easy maintenance and extension

## 📋 Prerequisites

- **Python 3.8+**
- **Poetry** (for dependency management) - [Install Poetry](https://python-poetry.org/docs/#installation)
- **Google Gemini API Key** - [Get your free API key](https://makersuite.google.com/app/apikey)

## 🚀 Quick Start with Poetry (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/shaheroumwali/langchain-playground.git
cd langchain-playground
```

### 2. Install Poetry (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install Dependencies
```bash
poetry install
```

This will create a virtual environment and install all dependencies with locked versions.

### 4. Configure Environment Variables
Copy the example file and add your API key:
```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 5. Run the Application
```bash
poetry run python main.py
```

Or use the built-in command:
```bash
poetry run start
```

The server will start at `http://localhost:8085`

## 🔧 Alternative: Using pip with requirements.txt

If you prefer not to use Poetry:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
python main.py
```

## 📚 API Endpoints

### 1. Send a Message
```bash
curl -X POST "http://localhost:8085/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "How do I write a for loop in Python?",
    "topic": "loops"
  }'
```

**Response:**
```json
{
  "response": "A for loop in Python iterates over a sequence..."
}
```

### 2. Get Conversation History
```bash
curl "http://localhost:8085/chat/user123"
```

**Response:**
```json
{
  "user_id": "user123",
  "history": [
    {"role": "user", "content": "How do I write a for loop in Python?"},
    {"role": "assistant", "content": "A for loop in Python iterates..."}
  ]
}
```

### 3. Clear Conversation History
```bash
curl -X DELETE "http://localhost:8085/chat/user123"
```

**Response:**
```json
{
  "status": "success",
  "message": "Cleared history for user user123"
}
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
# Required: Your Google Gemini API Key
GOOGLE_API_KEY=your_api_key_here

# Optional: Model configuration
MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.7

# Optional: System prompt
SYSTEM_MESSAGE=You are a helpful Python tutor who explains concepts clearly.
```

Get your API key: https://makersuite.google.com/app/apikey

## 📁 Project Structure

```
langchain-playground/
├── api/                    # FastAPI routes and handlers
│   ├── __init__.py
│   └── routes.py           # All API endpoints
├── config/                 # Configuration management
│   ├── __init__.py
│   └── settings.py         # Settings and API key loading
├── models/                 # Pydantic request/response models
│   ├── __init__.py
│   ├── requests.py         # Input validation
│   └── responses.py        # Output structures
├── services/               # Business logic
│   ├── __init__.py
│   ├── llm_service.py      # LLM and prompt management
│   └── memory_service.py   # Conversation memory (SQLite)
├── utils/                  # Helper utilities
│   ├── __init__.py
│   └── helpers.py          # Response truncation, etc.
├── main.py                 # FastAPI app entry point
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # pip dependencies (alternative)
├── .env.example            # Environment variables template
├── CODE_REVIEW.md          # Code review documentation
└── README.md               # This file
```

## 👨‍💻 Development

### Run with Poetry

Start the development server:
```bash
poetry run start
```

Run tests:
```bash
poetry run test
```

Format code:
```bash
poetry run format
```

Lint code:
```bash
poetry run lint
```

Type checking:
```bash
poetry run type-check
```

### Update Dependencies

To update dependencies while preserving compatibility:
```bash
poetry update
```

To add a new package:
```bash
poetry add package-name
```

## 🧪 Testing

Test data is saved to `chat_history.db` (SQLite database).

Example test flow:
```bash
# Send a message
curl -X POST "http://localhost:8085/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user", "message": "Explain list comprehension"}'

# Check history
curl "http://localhost:8085/chat/test-user"

# Clear history
curl -X DELETE "http://localhost:8085/chat/test-user"
```

## 🔗 Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8085/docs
- **ReDoc**: http://localhost:8085/redoc

## 📝 Notes

- Responses are truncated to 500 characters by default
- Each user maintains separate conversation history
- LLM is configured for concise outputs (`max_output_tokens=150`)
- Database uses SQLite for portability

To adjust output length, edit `services/llm_service.py`:
```python
max_output_tokens=150,  # Increase for longer responses
```

And in `api/routes.py`:
```python
truncate_response(response, 500)  # Increase for longer responses
```

## 🚀 Deployment

For production deployment:

1. Set `GOOGLE_API_KEY` environment variable securely
2. Use production ASGI server (e.g., Gunicorn with Uvicorn workers)
3. Add authentication/authorization as needed
4. Set up proper logging and monitoring
5. Use a persistent database solution (PostgreSQL recommended)

Example production run:
```bash
poetry run gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## 📖 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Poetry Documentation](https://python-poetry.org/docs/)

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Shah E Rome Wali**
- Email: shaheroumwali@gmail.com
- GitHub: [@shaheroumwali](https://github.com/shaheroumwali)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Last Updated**: 2024