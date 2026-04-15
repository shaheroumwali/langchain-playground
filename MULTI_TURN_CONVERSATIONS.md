# 🔄 Multi-Turn Conversations with Helper Messages

Enhanced multi-turn conversation support with intelligent context awareness and helper messages.

## 📋 Overview

This system provides sophisticated conversation management with:
- **Helper Messages** - Context-aware system prompts for better responses
- **Conversation Analytics** - Track topics, turn counts, and conversation stats
- **Message Formatting** - Professional formatting for conversation history
- **Context Enrichment** - Automatic context awareness across turns
- **Conversation Export** - Export conversations in multiple formats

---

## 🏗️ Architecture

```
ConversationHelper Service
├── ConversationContext
│   ├── extract_key_topics()
│   ├── format_conversation_summary()
│   └── get_last_n_turns()
├── MessageFormatter
│   ├── format_chat_history()
│   ├── format_context_message()
│   └── create_langchain_messages()
├── ConversationEnricher
│   ├── add_turn_counter()
│   ├── add_context_awareness()
│   └── generate_helper_prompt()
└── Enhanced LLM Service
    ├── send_message()
    └── send_message_with_helper_context()
```

---

## 🎯 Key Components

### 1. ConversationContext
Manages conversation state and extracts insights.

```python
context = ConversationContext(user_id="user123")

# Extract topics from conversation
topics = context.extract_key_topics(history)

# Get conversation summary
summary = context.format_conversation_summary(history)

# Get last N turns
recent_turns = context.get_last_n_turns(history, n=3)
```

### 2. MessageFormatter
Formats messages for optimal LLM processing.

```python
# Format history as readable string
formatted = MessageFormatter.format_chat_history(history)

# Create context message
context_msg = MessageFormatter.format_context_message(history, current_input)

# Convert to LangChain messages
messages = MessageFormatter.create_langchain_messages(history, current_input)
```

### 3. ConversationEnricher
Enhances conversations with metadata.

```python
# Add turn information
turn_info = ConversationEnricher.add_turn_counter(history)

# Add context awareness
context = ConversationEnricher.add_context_awareness(history, user_input)

# Generate comprehensive helper prompt
helper = ConversationEnricher.generate_helper_prompt(history, input, context)
```

---

## 📡 API Endpoints

### Chat Endpoints

#### 1. Send Message (POST)
**Endpoint**: `POST /chat`

**Request**:
```json
{
  "user_id": "user123",
  "message": "What is a Python function?",
  "topic": "functions"
}
```

**Response**:
```json
{
  "response": "A function is a reusable block of code..."
}
```

**Helper Features**:
- Automatic conversation history retrieval
- Turn counter included in context
- Topic extraction for conversation awareness
- Multi-turn context building

---

#### 2. Get Conversation History (GET)
**Endpoint**: `GET /chat/{user_id}`

**Response**:
```json
{
  "user_id": "user123",
  "history": [
    {"role": "user", "content": "What is a function?"},
    {"role": "assistant", "content": "A function is..."}
  ]
}
```

---

#### 3. Get Conversation Stats (GET)
**Endpoint**: `GET /chat/{user_id}/stats`

**Response**:
```json
{
  "status": "success",
  "data": {
    "user_id": "user123",
    "total_messages": 10,
    "user_messages": 5,
    "assistant_messages": 5,
    "total_characters": 1245,
    "avg_message_length": 124.5,
    "conversation_started": "2024-04-14 15:30:00",
    "last_message_time": "2024-04-14 15:45:00"
  }
}
```

---

#### 4. Get Conversation Topics (GET)
**Endpoint**: `GET /chat/{user_id}/topics`

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "topics": {
    "function": 5,
    "loop": 3,
    "variable": 2,
    "list": 1
  },
  "total_topics": 4
}
```

---

#### 5. Get Helper Context (GET)
**Endpoint**: `GET /chat/{user_id}/helper-context`

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "turn_count": 5,
  "conversation_summary": "Conversation summary: 5 user questions, discussing topics: function, loop, variable.",
  "key_topics": ["function", "loop", "variable"],
  "helper_info": "This is turn 5 of the conversation.",
  "message_count": 10
}
```

---

#### 6. Get Last N Messages (GET)
**Endpoint**: `GET /chat/{user_id}/last-n?n=5`

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "count": 5,
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

---

#### 7. Export Conversation (GET)
**Endpoint**: `GET /chat/{user_id}/export?format=markdown`

**Formats Available**:
- `text` - Plain text format
- `markdown` - Markdown format
- `json` - JSON format

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "format": "markdown",
  "conversation": "# Conversation History\n\n**User** _(at 2024-04-14 15:30:00)_\n\n> What is a Python function?..."
}
```

---

## 💡 Multi-Turn Conversation Features

### 1. Turn Counter
Automatically tracks which turn of the conversation you're on.

```
Turn #1: Initial question
Turn #2: Follow-up or new topic
Turn #3: Elaboration
...
```

### 2. Topic Extraction
Automatically identifies and tracks topics being discussed.

```
Topics discussed:
- Python (5 mentions)
- Functions (3 mentions)
- Loops (2 mentions)
```

### 3. Conversation Summary
Generates a summary of the conversation so far.

```
"Conversation summary: 5 user questions, discussing topics: function, loop, variable."
```

### 4. Context Awareness
Builds context automatically from previous exchanges.

```
"Building on previous response about the topic. Current question: ..."
```

### 5. Message Formatting
Professional formatting of conversation history for the LLM.

```
Previous conversation:
1. User: What is a function?
2. Assistant: A function is a reusable block of code...
3. User: How do I define one?
4. Assistant: You use the def keyword...
```

---

## 🚀 Usage Examples

### Example 1: Multi-Turn Python Tutor Conversation

```bash
# Turn 1: Ask about functions
curl -X POST "http://localhost:8085/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student1",
    "message": "What is a Python function?",
    "topic": "functions"
  }'

# Turn 2: Ask a follow-up
curl -X POST "http://localhost:8085/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student1",
    "message": "How do I define one?",
    "topic": "functions"
  }'

# Turn 3: Ask another related question
curl -X POST "http://localhost:8085/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student1",
    "message": "Can functions return multiple values?",
    "topic": "functions"
  }'
```

### Example 2: Get Conversation Analytics

```bash
# Get conversation statistics
curl "http://localhost:8085/chat/student1/stats"

# Get topics discussed
curl "http://localhost:8085/chat/student1/topics"

# Get helper context info
curl "http://localhost:8085/chat/student1/helper-context"

# Get last 5 messages
curl "http://localhost:8085/chat/student1/last-n?n=5"
```

### Example 3: Export Conversation

```bash
# Export as Markdown
curl "http://localhost:8085/chat/student1/export?format=markdown" > conversation.md

# Export as JSON
curl "http://localhost:8085/chat/student1/export?format=json" > conversation.json

# Export as Text
curl "http://localhost:8085/chat/student1/export?format=text" > conversation.txt
```

---

## 🔧 Configuration

### LLM Service Configuration

The helper messages are created with an enhanced system prompt:

```python
IMPORTANT CONVERSATION GUIDELINES:
- You are having a multi-turn conversation with the user
- Remember context from previous messages
- Build on previous explanations if relevant
- If the user asks a follow-up question, connect it to the previous discussion
- Provide concise but thorough answers
- Use examples when helpful
- Clarify any ambiguous questions
```

### Database Schema

```sql
-- Conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,           -- 'user' or 'assistant'
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table (tracks user sessions)
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    first_message DATETIME,
    last_message DATETIME,
    message_count INTEGER
);
```

---

## 📊 Supported Keywords

The helper system automatically extracts and tracks these Python-related keywords:

```
python, loop, function, class, variable, list, dictionary, 
string, method, module, import, exception, error
```

---

## ✅ Quality Assurance

All code passes:
- ✅ **Flake8** Linting (0 errors)
- ✅ **MyPy** Type Checking
- ✅ **Application Testing**

---

## 🎁 Benefits

1. **Better Context Understanding**
   - LLM knows what turn of conversation you're on
   - Previous context automatically included
   - Topics tracked for better responses

2. **Conversation Analytics**
   - Understand discussion patterns
   - Track learning topics
   - Monitor engagement

3. **Professional Export**
   - Save conversations in multiple formats
   - Share with others
   - Document learning progress

4. **Enhanced User Experience**
   - Smoother conversation flow
   - Better understanding of context
   - More coherent multi-turn interactions

---

## 🔮 Future Enhancements

Possible future additions:
- Conversation similarity detection
- Automatic conversation categorization
- User learning progress tracking
- Conversation recommendations
- Integration with external knowledge bases
- Advanced context summarization

---

## 📝 Files Modified/Created

**New Files**:
- `services/conversation_helper.py` - Helper classes and functions
- `MULTI_TURN_CONVERSATIONS.md` - This documentation

**Modified Files**:
- `services/llm_service.py` - Enhanced with helper message support
- `services/memory_service.py` - Added analytics methods
- `api/routes.py` - New endpoints for helper features

---

## 🏁 Summary

Multi-turn conversations are now fully enhanced with:
- ✅ Intelligent helper messages
- ✅ Conversation context awareness
- ✅ Comprehensive analytics
- ✅ Multiple export formats
- ✅ Professional message formatting
- ✅ Topic extraction and tracking

**Status**: ✅ Production Ready

---

**Last Updated**: April 14, 2026
