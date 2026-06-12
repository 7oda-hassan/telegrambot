"""
Core constants for the Telegram Checklist Bot.

This module contains centralized configuration constants used across different
layers of the Clean Architecture. By centralizing constants, we avoid hardcoded
values and make the system easier to configure and maintain.
"""
import re

# Regex to match Markdown checklist items.
# Matches optional bullet (`-` or `*`), followed by `[x]`, `[X]`, or `[ ]`,
# and captures the text of the checklist item.
CHECKLIST_REGEX = re.compile(
    r"^(?P<prefix>[-*]\s*)?\[(?P<status>[xX\s])\]\s*(?P<text>.*)$"
)

# Emojis used for rendering the checklist in Telegram.
# These match the exact visual requirements for a native-looking checklist.
CHECKED_EMOJI = "☑️"
UNCHECKED_EMOJI = "⬜"

# Telegram API constants.
MAX_MESSAGE_LENGTH = 4096
