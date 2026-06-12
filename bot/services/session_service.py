"""
session_service.py

Lightweight state management for user sessions.
"""

user_modes = {}

def set_markdown_mode(user_id: int, mode: bool):
    """Activates or deactivates markdown processing mode for a user."""
    user_modes[user_id] = mode

def is_markdown_mode(user_id: int) -> bool:
    """Checks if the user is currently in markdown processing mode."""
    return user_modes.get(user_id, False)
