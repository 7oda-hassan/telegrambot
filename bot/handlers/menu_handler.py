"""
menu_handler.py

Processes inline keyboard callbacks from the dynamic Role-Based /start menu.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.services.channel_service import ChannelService
from bot.services.session_service import set_markdown_mode
from bot.middlewares.auth import require_owner, require_admin
import bot.services.database as db
import logging

logger = logging.getLogger("telegram_bot.handlers.menu")
router = Router(name="menu_router")
channel_service = ChannelService()

@router.callback_query(F.data == "menu_markdown")
async def on_menu_markdown(callback: CallbackQuery):
    """Starts markdown mode directly from the menu."""
    set_markdown_mode(callback.from_user.id, True)
    text = (
        "📝 Markdown Mode Activated\n\n"
        "Send the markdown content you want to convert.\n"
        "The next message you send will be processed and converted into a Telegram Rich Message preview.\n"
        "Use /cancel to abort."
    )
    await callback.message.reply(text)
    await callback.answer()

@router.callback_query(F.data == "menu_publish")
@require_admin
async def on_menu_publish(callback: CallbackQuery):
    """Instructional prompt for publishing."""
    await callback.answer("To publish content, first start a Markdown session, generate a preview, and click Publish.", show_alert=True)

@router.callback_query(F.data == "menu_add_admin")
@require_owner
async def on_menu_add_admin(callback: CallbackQuery):
    await callback.answer("To add an admin, send: /add_admin <user_id>", show_alert=True)

@router.callback_query(F.data == "menu_remove_admin")
@require_owner
async def on_menu_remove_admin(callback: CallbackQuery):
    await callback.answer("To remove an admin, send: /remove_admin <user_id>", show_alert=True)

@router.callback_query(F.data == "menu_list_admins")
@require_owner
async def on_menu_list_admins(callback: CallbackQuery):
    admins = db.get_admins()
    if not admins:
        text = "No admins added."
    else:
        text = "👔 **Authorized Admins:**\n" + "\n".join([f"- `{uid}`" for uid in admins])
    await callback.message.reply(text, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "menu_manage_channels")
@require_owner
async def on_menu_manage_channels(callback: CallbackQuery):
    await callback.answer("To add: /add_channel @username\nTo remove: /remove_channel <id>", show_alert=True)

@router.callback_query(F.data == "menu_list_channels")
@require_admin
async def on_menu_list_channels(callback: CallbackQuery):
    channels = db.get_channels()
    if not channels:
        text = "No channels linked. Add one with `/add_channel`"
    else:
        text = "📢 **Linked Channels:**\n\n"
        for c in channels:
            text += f"- {c['channel_name']} (`{c['channel_id']}`)\n"
    await callback.message.reply(text, parse_mode="Markdown")
    await callback.answer()
