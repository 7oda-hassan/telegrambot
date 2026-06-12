"""
bot/services/channel_service.py

Business logic orchestrator for channel publishing features.
Handles validation, permissions, and publishing operations.
"""
import os
import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
import bot.services.database as db
from bot.api.send_rich_message import SendRichMessage, InputRichMessage

logger = logging.getLogger("telegram_bot.services.channel")

class ChannelService:
    def __init__(self):
        self.owner_id = int(os.getenv("OWNER_ID", "0"))

    def is_owner(self, user_id: int) -> bool:
        """Checks if the user is the bot owner."""
        return user_id == self.owner_id

    def is_authorized(self, user_id: int) -> bool:
        """Checks if the user is authorized to publish (Owner or Admin)."""
        if self.is_owner(user_id):
            return True
        return user_id in db.get_admins()

    async def add_channel_if_valid(self, bot: Bot, channel_id_or_username: str) -> tuple[bool, str]:
        """
        Validates if the bot can post to the channel before adding it.
        Returns (success: bool, message: str)
        """
        try:
            # Fetch channel info
            chat = await bot.get_chat(channel_id_or_username)
            if chat.type != "channel":
                return False, f"❌ {channel_id_or_username} is not a channel."
                
            # Verify bot permissions
            member = await bot.get_chat_member(chat.id, bot.id)
            if member.status not in ("administrator", "creator") or not getattr(member, 'can_post_messages', False):
                return False, f"❌ Bot is not an administrator in {chat.title} or cannot post messages."
                
            # Add to DB
            if db.add_channel(str(chat.id), chat.title):
                logger.info(f"Added channel {chat.title} ({chat.id})")
                return True, f"✅ Successfully added channel: {chat.title}"
            else:
                return False, f"⚠️ Channel {chat.title} is already added."
                
        except (TelegramBadRequest, TelegramForbiddenError) as e:
            return False, f"❌ Could not access channel {channel_id_or_username}. Ensure the bot is added as an admin. Error: {e}"
        except Exception as e:
            logger.error(f"Error adding channel {channel_id_or_username}: {e}")
            return False, "❌ An unexpected error occurred while verifying the channel."

    async def publish_message(self, bot: Bot, channel_id: str, markdown: str) -> tuple[bool, str]:
        """
        Publishes the explicitly provided markdown directly to a channel.
        This DOES NOT re-parse content. It simply wraps it in the SendRichMessage payload.
        """
        try:
            method = SendRichMessage(
                chat_id=channel_id,
                rich_message=InputRichMessage(markdown=markdown)
            )
            await bot(method)
            logger.info(f"Successfully published message to channel {channel_id}")
            return True, "✅ Content published successfully."
        except Exception as e:
            logger.error(f"Failed to publish to channel {channel_id}: {e}")
            return False, "❌ Failed to publish content. Please try again."
