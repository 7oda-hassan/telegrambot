"""
bot/middlewares/auth.py

Provides reusable decorator-based access control middleware 
for owner and admin authorization checks.
"""
from functools import wraps
from aiogram.types import Message, CallbackQuery
from bot.services.channel_service import ChannelService

channel_service = ChannelService()

def require_owner(func):
    """Decorator to require Owner privileges for a handler."""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        user_id = event.from_user.id
        if not channel_service.is_owner(user_id):
            msg = "❌ You do not have permission to use this command."
            if isinstance(event, Message):
                await event.reply(msg)
            elif isinstance(event, CallbackQuery):
                await event.answer(msg, show_alert=True)
            return
        return await func(event, *args, **kwargs)
    return wrapper

def require_admin(func):
    """Decorator to require Admin or Owner privileges for a handler."""
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        user_id = event.from_user.id
        if not channel_service.is_authorized(user_id):
            msg = "❌ You do not have permission to use this command."
            if isinstance(event, Message):
                await event.reply(msg)
            elif isinstance(event, CallbackQuery):
                await event.answer(msg, show_alert=True)
            return
        return await func(event, *args, **kwargs)
    return wrapper
