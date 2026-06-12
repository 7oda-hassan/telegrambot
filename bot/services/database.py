"""
bot/services/database.py

Lightweight SQLite database wrapper for channel and admin management.
Uses the standard library sqlite3 to avoid heavy dependencies.
"""
import sqlite3
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("telegram_bot.services.database")

DB_PATH = "data/bot_database.sqlite"

def init_db():
    """Initializes the database and creates required tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Channels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                channel_id TEXT PRIMARY KEY,
                channel_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Drafts table (transient message cache for publishing)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drafts (
                message_id INTEGER,
                chat_id INTEGER,
                markdown TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (message_id, chat_id)
            )
        ''')
        
        conn.commit()
    logger.info("Database initialized successfully.")

# --- Channel CRUD ---

def add_channel(channel_id: str, channel_name: str) -> bool:
    """Adds a channel. Returns False if it already exists."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO channels (channel_id, channel_name) VALUES (?, ?)", (str(channel_id), channel_name))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def remove_channel(channel_id: str) -> bool:
    """Removes a channel. Returns True if deleted."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM channels WHERE channel_id = ?", (str(channel_id),))
        conn.commit()
        return cursor.rowcount > 0

def get_channels() -> List[Dict[str, str]]:
    """Returns a list of all linked channels."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT channel_id, channel_name FROM channels ORDER BY created_at ASC")
        return [{"channel_id": row[0], "channel_name": row[1]} for row in cursor.fetchall()]

# --- Admin CRUD ---

def add_admin(user_id: int) -> bool:
    """Adds an admin. Returns False if already admin."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def remove_admin(user_id: int) -> bool:
    """Removes an admin. Returns True if deleted."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_admins() -> List[int]:
    """Returns a list of admin user IDs."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT user_id FROM admins")
        return [row[0] for row in cursor.fetchall()]

# --- Drafts CRUD (for publishing) ---

def save_draft(message_id: int, chat_id: int, markdown: str):
    """Caches the generated markdown for a specific message."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO drafts (message_id, chat_id, markdown) VALUES (?, ?, ?)",
            (message_id, chat_id, markdown)
        )
        conn.commit()

def get_draft(message_id: int, chat_id: int) -> Optional[str]:
    """Retrieves cached markdown draft."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT markdown FROM drafts WHERE message_id = ? AND chat_id = ?", (message_id, chat_id))
        row = cursor.fetchone()
        return row[0] if row else None

def delete_draft(message_id: int, chat_id: int):
    """Deletes a cached draft."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM drafts WHERE message_id = ? AND chat_id = ?", (message_id, chat_id))
        conn.commit()
