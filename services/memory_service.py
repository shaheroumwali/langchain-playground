import sqlite3
from typing import List, Tuple, Dict, Any
from datetime import datetime


class SimpleMemory:
    """A simple conversation memory implemented for the demo."""

    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append((role, content))

    def get_history(self):
        history = []
        for role, content in self.messages:
            if role == "user":
                history.append(("user", content))
            else:
                history.append(("assistant", content))
        return history

    def clear(self):
        self.messages = []

    def show(self):
        print("\n📦 Memory contents:")
        if not self.messages:
            print("  (empty)")
            return
        for i, (role, content) in enumerate(self.messages, 1):
            print(f"  {i}. {role}: {content[:80]}...")
        print()


class SQLiteMemory:
    """SQLite-backed conversation memory with user session support and analytics."""

    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_id ON conversations(user_id)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)
        ''')
        
        # Create sessions table for tracking conversations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                first_message DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_message DATETIME DEFAULT CURRENT_TIMESTAMP,
                message_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()

    def add_message(self, user_id: str, role: str, content: str):
        """Store message in database and update session info."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Add message
        cursor.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        
        # Update or create session
        cursor.execute(
            "SELECT id FROM sessions WHERE user_id = ?",
            (user_id,)
        )
        
        if cursor.fetchone():
            # Update existing session
            cursor.execute(
                "UPDATE sessions SET last_message = CURRENT_TIMESTAMP, "
                "message_count = message_count + 1 WHERE user_id = ?",
                (user_id,)
            )
        else:
            # Create new session
            cursor.execute(
                "INSERT INTO sessions (user_id, message_count) VALUES (?, 1)",
                (user_id,)
            )
        
        conn.commit()
        conn.close()

    def get_history(self, user_id: str) -> List[Tuple[str, str]]:
        """Retrieve conversation history for user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY timestamp",
            (user_id,)
        )
        history = cursor.fetchall()
        conn.close()
        return history

    def get_history_with_timestamps(self, user_id: str) -> List[Tuple[str, str, str]]:
        """Retrieve conversation history with timestamps."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM conversations WHERE user_id = ? ORDER BY timestamp",
            (user_id,)
        )
        history = cursor.fetchall()
        conn.close()
        return history

    def get_last_n_messages(self, user_id: str, n: int = 10) -> List[Tuple[str, str]]:
        """Get the last n messages from user's history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM conversations WHERE user_id = ? "
            "ORDER BY timestamp DESC LIMIT ?",
            (user_id, n)
        )
        history = list(reversed(cursor.fetchall()))
        conn.close()
        return history

    def get_conversation_stats(self, user_id: str) -> Dict[str, Any]:
        """Get statistics about user's conversation."""
        history = self.get_history_with_timestamps(user_id)
        
        if not history:
            return {
                "user_id": user_id,
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "total_characters": 0,
                "avg_message_length": 0,
                "conversation_started": None
            }
        
        user_msgs = [h for h in history if h[0] == "user"]
        assistant_msgs = [h for h in history if h[0] == "assistant"]
        total_chars = sum(len(h[1]) for h in history)
        
        stats = {
            "user_id": user_id,
            "total_messages": len(history),
            "user_messages": len(user_msgs),
            "assistant_messages": len(assistant_msgs),
            "total_characters": total_chars,
            "avg_message_length": total_chars / len(history) if history else 0,
            "conversation_started": history[0][2] if history else None,
            "last_message_time": history[-1][2] if history else None,
        }
        
        return stats

    def get_conversation_topics(self, user_id: str) -> Dict[str, int]:
        """Extract topics from conversation."""
        history = self.get_history(user_id)
        
        keywords = {
            "python": 0,
            "loop": 0,
            "function": 0,
            "class": 0,
            "variable": 0,
            "list": 0,
            "dictionary": 0,
            "string": 0,
            "method": 0,
            "module": 0,
            "import": 0,
            "exception": 0,
            "error": 0,
        }
        
        for role, content in history:
            content_lower = content.lower()
            for keyword in keywords:
                if keyword in content_lower:
                    keywords[keyword] += 1
        
        # Return only non-zero topics, sorted by count
        return dict(sorted(
            {k: v for k, v in keywords.items() if v > 0}.items(),
            key=lambda x: x[1],
            reverse=True
        ))

    def clear(self, user_id: str):
        """Clear user's conversation history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    def show(self, user_id: str):
        """Display user's conversation history."""
        history = self.get_history(user_id)
        print(f"\n📦 Memory contents for user {user_id}:")
        if not history:
            print("  (empty)")
            return
        for i, (role, content) in enumerate(history, 1):
            print(f"  {i}. {role}: {content[:80]}...")
        print()

    def export_conversation(self, user_id: str, format: str = "text") -> str:
        """Export conversation in different formats."""
        history = self.get_history_with_timestamps(user_id)
        
        if format == "text":
            return self._export_as_text(history)
        elif format == "markdown":
            return self._export_as_markdown(history)
        elif format == "json":
            return self._export_as_json(history)
        else:
            return self._export_as_text(history)

    def _export_as_text(self, history: List[Tuple[str, str, str]]) -> str:
        """Export conversation as plain text."""
        text = "Conversation History\n" + "=" * 50 + "\n\n"
        for role, content, timestamp in history:
            role_label = "USER" if role == "user" else "ASSISTANT"
            text += f"[{role_label}] {timestamp}\n{content}\n\n"
        return text

    def _export_as_markdown(self, history: List[Tuple[str, str, str]]) -> str:
        """Export conversation as Markdown."""
        md = "# Conversation History\n\n"
        for i, (role, content, timestamp) in enumerate(history, 1):
            if role == "user":
                md += f"**User** _(at {timestamp})_\n\n> {content}\n\n"
            else:
                md += f"**Assistant** _(at {timestamp})_\n\n{content}\n\n"
        return md

    def _export_as_json(self, history: List[Tuple[str, str, str]]) -> str:
        """Export conversation as JSON."""
        import json
        json_data = [
            {"role": role, "content": content, "timestamp": timestamp}
            for role, content, timestamp in history
        ]
        return json.dumps(json_data, indent=2)
