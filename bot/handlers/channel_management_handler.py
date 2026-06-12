"""
bot/handlers/channel_management_handler.py

Owner/Admin commands to manage linked channels and bot administrators.
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import bot.services.database as db
from bot.services.channel_service import ChannelService
from bot.middlewares.auth import require_owner, require_admin
import logging

logger = logging.getLogger("telegram_bot.handlers.channel_management")
router = Router(name="channel_management_router")
channel_service = ChannelService()

# --- Admin Management (Owner Only) ---

@router.message(Command("add_admin"))
@require_owner
async def cmd_add_admin(message: Message):
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        return await message.reply("Usage: `/add_admin <user_id>`", parse_mode="Markdown")
        
    user_id = int(args[1])
    if db.add_admin(user_id):
        logger.info(f"Admin added: {user_id}")
        await message.reply(f"✅ User `{user_id}` added as admin.", parse_mode="Markdown")
    else:
        await message.reply("⚠️ User is already an admin.")

@router.message(Command("remove_admin"))
@require_owner
async def cmd_remove_admin(message: Message):
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        return await message.reply("Usage: `/remove_admin <user_id>`", parse_mode="Markdown")
        
    user_id = int(args[1])
    if db.remove_admin(user_id):
        logger.info(f"Admin removed: {user_id}")
        await message.reply(f"✅ User `{user_id}` removed from admins.", parse_mode="Markdown")
    else:
        await message.reply("⚠️ User was not an admin.")

@router.message(Command("list_admins"))
@require_owner
async def cmd_list_admins(message: Message):
        
    admins = db.get_admins()
    if not admins:
        return await message.reply("No admins added.")
        
    text = "👔 **Authorized Admins:**\n" + "\n".join([f"- `{uid}`" for uid in admins])
    await message.reply(text, parse_mode="Markdown")


# --- Channel Management (Owner & Admins) ---

@router.message(Command("add_channel"))
@require_owner
async def cmd_add_channel(message: Message):
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: `/add_channel @channel_username` or `/add_channel -100...`", parse_mode="Markdown")
        
    channel_ref = args[1]
    wait_msg = await message.reply("⏳ Verifying channel permissions...")
    
    success, result_text = await channel_service.add_channel_if_valid(message.bot, channel_ref)
    await wait_msg.edit_text(result_text)

@router.message(Command("remove_channel"))
@require_owner
async def cmd_remove_channel(message: Message):
        
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("Usage: `/remove_channel <channel_id>`", parse_mode="Markdown")
        
    channel_id = args[1]
    if db.remove_channel(channel_id):
        logger.info(f"Channel removed: {channel_id}")
        await message.reply(f"✅ Channel `{channel_id}` removed.", parse_mode="Markdown")
    else:
        await message.reply("⚠️ Channel not found.")

@router.message(Command("list_channels"))
@require_admin
async def cmd_list_channels(message: Message):
        
    channels = db.get_channels()
    if not channels:
        return await message.reply("No channels linked. Add one with `/add_channel`", parse_mode="Markdown")
        
    text = "📢 **Linked Channels:**\n\n"
    for c in channels:
        text += f"- {c['channel_name']} (`{c['channel_id']}`)\n"
        
    await message.reply(text, parse_mode="Markdown")
