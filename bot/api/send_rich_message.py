from typing import Optional, Union, Any
from aiogram.methods.base import TelegramMethod
from aiogram.types import Message, TelegramObject, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

class InputRichMessage(TelegramObject):
    """
    Describes a rich message to be sent via the sendRichMessage API.
    Exactly one of the fields html or markdown must be used.
    """
    markdown: Optional[str] = None
    html: Optional[str] = None
    is_rtl: Optional[bool] = None
    skip_entity_detection: Optional[bool] = None

class SendRichMessage(TelegramMethod[Message]):
    """
    Custom API method to call Telegram's undocumented / new 'sendRichMessage' endpoint.
    This natively parses markdown checklists on the server side into interactive RichBlocks.
    """
    __api_method__ = "sendRichMessage"
    __returning__ = Message

    chat_id: Union[int, str]
    rich_message: InputRichMessage
    reply_to_message_id: Optional[int] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = None
