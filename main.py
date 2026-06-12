"""
Application entry point for the Telegram Checklist Bot.

This script initializes the environment, configures the Aiogram Bot and
Dispatcher instances, attaches middlewares and routers, and starts the
asynchronous polling loop.
"""
import asyncio
import os
import sys
import re
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

# Setup logger before importing other local modules
from utils.logger import logger
from bot.handlers.checklist_handler import router as checklist_router
from bot.handlers.channel_management_handler import router as channel_management_router
from bot.handlers.publish_handler import router as publish_router
from bot.handlers.session_handler import router as session_router
from bot.handlers.menu_handler import router as menu_router
from bot.middlewares.error_middleware import GlobalErrorMiddleware
import bot.services.database as db

def get_token() -> str:
    """
    Loads and validates the bot token from the environment.
    
    Returns:
        str: The Telegram Bot API token.
        
    Raises:
        ValueError: If the BOT_TOKEN environment variable is missing.
    """
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.critical("BOT_TOKEN is not set in the environment variables.")
        sys.exit(1)
        
    if not re.match(r"^[0-9]+:[a-zA-Z0-9_-]+$", token):
        logger.critical("BOT_TOKEN format is invalid. It must match standard Telegram token format.")
        sys.exit(1)
        
    return token

async def main():
    """
    Main asynchronous coroutine that initializes and runs the bot.
    
    It binds the global error middleware to catch unhandled exceptions,
    includes the checklist router for message handling, and starts polling
    while dropping any pending offline updates.
    """
    logger.info("Starting Telegram Bot...")
    db.init_db()
    
    token = get_token()
    bot = Bot(token=token)
    dp = Dispatcher()

    # Register Middlewares
    dp.update.outer_middleware(GlobalErrorMiddleware())

    # Register Routers (Handlers)
    dp.include_router(channel_management_router)
    dp.include_router(publish_router)
    dp.include_router(session_router)
    dp.include_router(menu_router)
    dp.include_router(checklist_router)

    try:
        me = await bot.get_me()
        logger.info(f"Bot started successfully! Username: @{me.username} | ID: {me.id}")
        logger.info("Bot is polling...")
        
        # Drop pending updates to avoid processing old messages
        await bot.delete_webhook(drop_pending_updates=True)
        # Aiogram start_polling inherently catches SIGINT/SIGTERM for graceful shutdown
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Critical error during polling: {e}", exc_info=True)
    finally:
        logger.info("Shutting down Telegram Bot cleanly...")
        await bot.session.close()
        logger.info("Resources released. Exit.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt).")
