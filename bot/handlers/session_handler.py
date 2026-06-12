"""
session_handler.py

Handles basic commands and session mode toggles (/start, /help, /markdown, /cancel).
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.services.session_service import set_markdown_mode
from bot.services.channel_service import ChannelService
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

logger = logging.getLogger("telegram_bot.handlers.session")
router = Router(name="session_router")
channel_service = ChannelService()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    builder = InlineKeyboardBuilder()
    
    if channel_service.is_owner(user_id):
        text = (
            "👋 Welcome Owner\n\n"
            "Available Actions:\n"
            "📝 Markdown Mode\n"
            "📢 Publish Content\n"
            "👥 Admin Management\n"
            "📺 Channel Management\n"
            "📋 List Channels\n"
            "📋 List Admins"
        )
        builder.button(text="📝 Start Markdown Session", callback_data="menu_markdown")
        builder.button(text="➕ Add Admin", callback_data="menu_add_admin")
        builder.button(text="➖ Remove Admin", callback_data="menu_remove_admin")
        builder.button(text="📋 List Admins", callback_data="menu_list_admins")
        builder.button(text="📺 Manage Channels", callback_data="menu_manage_channels")
        builder.button(text="📋 List Channels", callback_data="menu_list_channels")
        builder.button(text="📢 Publish Content", callback_data="menu_publish")
        builder.adjust(1, 2, 1, 2, 1) # Formatting rows
        
    elif channel_service.is_authorized(user_id):
        text = (
            "👋 Welcome Admin\n\n"
            "Available Actions:\n"
            "📝 Markdown Mode\n"
            "📢 Publish Content\n"
            "📋 View Channels"
        )
        builder.button(text="📝 Start Markdown Session", callback_data="menu_markdown")
        builder.button(text="📢 Publish Content", callback_data="menu_publish")
        builder.button(text="📋 List Channels", callback_data="menu_list_channels")
        builder.adjust(1)
        
    else:
        text = (
            "👋 Welcome\n\n"
            "Use:\n"
            "📝 Markdown Mode\n"
            "to start converting markdown content."
        )
        builder.button(text="📝 Start Markdown Session", callback_data="menu_markdown")
        builder.adjust(1)

    await message.reply(text, reply_markup=builder.as_markup())

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Available Commands:\n"
        "/markdown - Start a markdown conversion session\n"
        "/cancel - Cancel current markdown session\n"
        "/help - Show help\n\n"
        "Workflow:\n"
        "1. Run /markdown\n"
        "2. Send markdown content\n"
        "3. Receive Rich Message preview\n"
        "4. Optionally publish to a linked channel"
    )
    await message.reply(text)

@router.message(Command("markdown"))
async def cmd_markdown(message: Message):
    set_markdown_mode(message.from_user.id, True)
    text = (
        "📝 Markdown Mode Activated\n\n"
        "Send the markdown content you want to convert.\n"
        "The next message you send will be processed and converted into a Telegram Rich Message preview.\n"
        "Use /cancel to abort."
    )
    await message.reply(text)

@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    set_markdown_mode(message.from_user.id, False)
    await message.reply("❌ Markdown Mode Cancelled")
