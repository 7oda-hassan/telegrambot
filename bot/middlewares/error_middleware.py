"""
Global exception handling middleware.

This middleware intercepts all events processed by Aiogram. It prevents
unexpected exceptions from crashing the application and ensures the user
receives a graceful failure message.
"""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
import logging
from core.exceptions import BotBaseException

logger = logging.getLogger("telegram_bot.middlewares.error")

class GlobalErrorMiddleware(BaseMiddleware):
    """
    Middleware that catches unhandled exceptions globally.
    
    By wrapping the execution of every handler, we can catch specific business
    logic errors (BotBaseException) to send friendly messages, or catch
    critical system exceptions to log them safely without terminating the bot.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Executes the wrapped handler and catches any resulting exceptions.
        
        Args:
            handler: The next middleware or handler in the chain.
            event: The incoming Telegram update/event.
            data: Context data passed between middlewares.
            
        Returns:
            Any: The result of the handler, if successful.
        """
        try:
            return await handler(event, data)
        except BotBaseException as e:
            # Expected business logic errors
            logger.error(f"Business logic exception: {e}")
            if isinstance(event, Message):
                await event.reply("An error occurred while processing your message. Please try again.")
        except Exception as e:
            # Unexpected system errors
            user_id = event.from_user.id if hasattr(event, 'from_user') and event.from_user else "Unknown"
            text = event.text if isinstance(event, Message) and event.text else ""
            msg_snippet = text[:100] + ("..." if len(text) > 100 else "")
            
            error_log = f"\n[ERROR]\nUser ID: {user_id}\nMessage: {msg_snippet}\nException: {str(e)}"
            logger.error(error_log)
            
            if isinstance(event, Message):
                await event.reply("An unexpected error occurred while processing your message. Please try again.")
