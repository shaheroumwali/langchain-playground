import sqlite3
from typing import List, Tuple


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
    """SQLite-backed conversation memory with user session support."""

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
        conn.commit()
        conn.close()

    def add_message(self, user_id: str, role: str, content: str):
        """Store message in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
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

    def clear(self, user_id: str):
        """Clear user's conversation history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
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
