"""
bot/handlers/publish_handler.py

Handles the inline keyboard callback queries for publishing
generated Rich Messages to linked channels.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import bot.services.database as db
from bot.services.channel_service import ChannelService
from bot.middlewares.auth import require_admin
import logging

logger = logging.getLogger("telegram_bot.handlers.publish")
router = Router(name="publish_router")
channel_service = ChannelService()

@router.callback_query(F.data.startswith("publish_start:"))
@require_admin
async def on_publish_start(callback: CallbackQuery):
    """Triggered when the user clicks '✅ Publish' on the formatted message."""
    _, original_msg_id = callback.data.split(":", 1)
    
    channels = db.get_channels()
    if not channels:
        return await callback.answer("⚠️ No channels linked. Ask the Owner to add one.", show_alert=True)
        
    # Build channel selection keyboard
    builder = InlineKeyboardBuilder()
    for c in channels:
        # data: publish_send:<original_msg_id>:<channel_id>
        builder.button(text=f"📢 {c['channel_name']}", callback_data=f"publish_send:{original_msg_id}:{c['channel_id']}")
        
    builder.button(text="❌ Cancel", callback_data=f"publish_cancel:{original_msg_id}")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Select a destination channel to publish:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("publish_cancel:"))
@require_admin
async def on_publish_cancel(callback: CallbackQuery):
    """Triggered when the user clicks '❌ Cancel' either immediately or at channel selection."""
    _, original_msg_id = callback.data.split(":", 1)
    
    # Remove the reply_markup (inline keyboard) entirely and delete the prompt text
    # Wait, the prompt text replaced the original message text if it was a prompt.
    # Actually, the buttons were attached to a separate prompt message OR the rich message.
    # The requirement says: 
    # "After formatting: Bot sends: Formatted Rich Message. Then: 'Would you like to publish this content?'"
    # Ah, so the keyboard is on a SEPARATE message!
    
    # Let's clean up the prompt message
    await callback.message.delete()
    
    # Clean up the draft to free sqlite memory
    db.delete_draft(int(original_msg_id), callback.message.chat.id)

@router.callback_query(F.data.startswith("publish_send:"))
@require_admin
async def on_publish_send(callback: CallbackQuery):
    """Triggered when the user selects a specific channel to publish to."""
    parts = callback.data.split(":")
    original_msg_id = int(parts[1])
    channel_id = parts[2]
    
    # Retrieve draft
    markdown = db.get_draft(original_msg_id, callback.message.chat.id)
    if not markdown:
        await callback.message.edit_text("❌ Draft expired or not found.")
        return await callback.answer()
        
    # Attempt publish
    success, result_msg = await channel_service.publish_message(callback.bot, channel_id, markdown)
    
    if success:
        # Remove keyboard, show success
        await callback.message.edit_text(result_msg)
        # Clean up draft
        db.delete_draft(original_msg_id, callback.message.chat.id)
    else:
        # Keep keyboard to let them try again or cancel, but show error
        await callback.answer(result_msg, show_alert=True)
