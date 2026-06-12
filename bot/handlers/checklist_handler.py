"""
Telegram handlers for processing incoming checklist messages.

This module acts as the Controller in the Clean Architecture. It receives
the raw HTTP/Polling updates from Telegram via Aiogram, delegates the text
to the Use Case (MessageService), and sends the response back to the user.
"""
from aiogram import Router, F
from aiogram.types import Message
import logging
from bot.services.message_service import MessageService
from bot.api.send_rich_message import SendRichMessage, InputRichMessage
from aiogram.exceptions import TelegramBadRequest
import re
import os
import bot.services.database as db
from bot.services.channel_service import ChannelService
from bot.services.session_service import is_markdown_mode, set_markdown_mode
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger("telegram_bot.handlers.checklist")

router = Router(name="checklist_router")
message_service = MessageService()
channel_service = ChannelService()

@router.message(F.text)
async def handle_checklist_message(message: Message):
    """
    Handles all incoming text messages containing potential checklists.
    
    This function contains ZERO business logic. It relies entirely on the
    `MessageService` to parse and format the text. It uses `message.reply()`
    to quote the user's original message, exactly matching the visual
    requirements of the Markdown Editor.
    
    Args:
        message (Message): The Aiogram Message object representing the user input.
    """
    # Extract raw text from the message
    text = message.text or message.caption
    
    if not text or text.startswith("/"):
        return
        
    if not is_markdown_mode(message.from_user.id):
        return

    # Delegate parsing and formatting to the business logic layer
    formatted_reply = message_service.process_message(message)
    
    # Send the response directly using the custom RichMessage API hook
    if formatted_reply and formatted_reply.strip() != "":
        method = SendRichMessage(
            chat_id=message.chat.id,
            rich_message=InputRichMessage(markdown=formatted_reply)
        )
        try:
            sent_msg = await message.bot(method)
            
            # Prompt for publishing if authorized
            if channel_service.is_authorized(message.from_user.id):
                db.save_draft(sent_msg.message_id, message.chat.id, formatted_reply)
                
                builder = InlineKeyboardBuilder()
                builder.button(text="✅ Publish", callback_data=f"publish_start:{sent_msg.message_id}")
                builder.button(text="❌ Cancel", callback_data=f"publish_cancel:{sent_msg.message_id}")
                
                await message.answer(
                    "Would you like to publish this content?",
                    reply_markup=builder.as_markup()
                )
            
            # Automatically exit markdown mode upon success
            set_markdown_mode(message.from_user.id, False)
                
        except TelegramBadRequest as e:
            if "RICH_MESSAGE_PHOTO_URL_INVALID" in str(e):
                logger.warning(f"Invalid media URL detected in message for user {message.from_user.id}. Stripping invalid photos and retrying...")
                # Strip image extensions causing the crash while leaving text intact
                clean_reply = re.sub(r'\[([^\]]+)\]\([^)]+\.(?:jpg|jpeg|png|gif|webp)[^)]*\)', r'\1', formatted_reply, flags=re.IGNORECASE)
                
                # Retry sending the cleaned message using a new object
                new_method = SendRichMessage(
                    chat_id=message.chat.id,
                    rich_message=InputRichMessage(markdown=clean_reply)
                )
                sent_msg = await message.bot(new_method)
                
                if channel_service.is_authorized(message.from_user.id):
                    db.save_draft(sent_msg.message_id, message.chat.id, clean_reply)
                    
                    builder = InlineKeyboardBuilder()
                    builder.button(text="✅ Publish", callback_data=f"publish_start:{sent_msg.message_id}")
                    builder.button(text="❌ Cancel", callback_data=f"publish_cancel:{sent_msg.message_id}")
                    
                    await message.answer(
                        "Would you like to publish this content?",
                        reply_markup=builder.as_markup()
                    )
                
                # Automatically exit markdown mode upon success
                set_markdown_mode(message.from_user.id, False)
            else:
                logger.error(f"Failed to process markdown message: {e}")
                await message.reply("❌ Markdown processing failed. Please try again or type /cancel.")
                raise e
