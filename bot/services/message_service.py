"""
Application service bridging handlers and domain logic.

The MessageService acts as the primary Use Case orchestrator in the Clean
Architecture. It coordinates between the ParserFactory and the Formatters,
ensuring the Telegram handlers remain completely devoid of business logic.
"""
from parsers.core.entity_builder import EntityASTBuilder
from parsers.core.plugin_loader import load_all_plugins
from formatters.telegram_rich_formatter import TelegramRichMessageFormatter
from core.exceptions import BotBaseException
from aiogram.types import Message
import logging

logger = logging.getLogger("telegram_bot.services.message")

class MessageService:
    """
    Service class responsible for processing user text.
    
    It handles the workflow of:
    1. Fetching the correct parser from the factory.
    2. Parsing the raw input text.
    3. Formatting the parsed elements using a designated formatter.
    """
    
    def __init__(self):
        """
        Initializes the MessageService with the required formatter.
        In a more advanced setup, the formatter could be injected via Dependency Injection.
        """
        self.formatter = TelegramRichMessageFormatter()
        # Ensure block-level Tokenizer plugins are loaded once globally
        load_all_plugins()

    def process_message(self, message: Message) -> str:
        """
        Main entry point for processing an incoming Telegram Message.
        It converts the pre-parsed Telegram entities directly into the internal AST.
        """
        try:
            # Extract text and entities
            text = message.text or message.caption or ""
            entities = message.entities or message.caption_entities or []
            
            builder = EntityASTBuilder(text, entities)
            ast_root = builder.build()
            
            formatted_text = self.formatter.format(ast_root)
            
            return formatted_text
        except Exception as e:
            logger.error(f"Error processing text: {e}", exc_info=True)
            raise BotBaseException("Failed to process the message.") from e
