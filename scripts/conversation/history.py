import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage


class MessageModel(BaseModel):
    id: int
    session_id: str
    ai_message: Optional[str]
    human_message: Optional[str]
    created_at: datetime


class MessageHistory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS message_store (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    ai_message TEXT,
                    human_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_message(self, session_id: str, ai_message: Optional[str] = None, human_message: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO message_store (session_id, ai_message, human_message, created_at) 
                VALUES (?, ?, ?, ?)
            ''', (session_id, ai_message, human_message, datetime.now()))
            conn.commit()

    def get_messages(self, k: Optional[int] = None) -> List[MessageModel]:
        query = 'SELECT id, session_id, ai_message, human_message, created_at FROM message_store ORDER BY created_at DESC'
        if k is not None:
            query += f' LIMIT {k}'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            messages = cursor.fetchall()

        return [MessageModel(id=id, session_id=session_id, ai_message=ai_message, human_message=human_message, created_at=created_at)
                for id, session_id, ai_message, human_message, created_at in messages]

    def get_messages_by_session_id(self, session_id: str, k: Optional[int] = 3) -> List[BaseMessage]:
        query = 'SELECT id, session_id, ai_message, human_message, created_at FROM message_store WHERE session_id = ? ORDER BY id DESC'
        if k is not None:
            query += f' LIMIT {k}'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (session_id,))
            messages = cursor.fetchall()

        reversed_messages = list(reversed(messages))
        history_messages = []
        for _, _, ai_message, human_message, _ in reversed_messages:
            history_messages.append(HumanMessage(content=human_message))
            history_messages.append(AIMessage(content=ai_message))
        return history_messages

    def build_chat_history(self, session_id: str, k: Optional[int] = None) -> Optional[str]:
        messages = self.get_messages_by_session_id(session_id, k)
        if len(messages) == 0:
            return None
        history = []
        for msg in messages:
            if msg.human_message:
                history.append(f"human: {msg.human_message}")
            if msg.ai_message:
                history.append(f"ai: {msg.ai_message}")
        return "\n\n".join(history)
