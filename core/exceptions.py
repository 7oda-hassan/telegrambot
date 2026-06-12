"""
Core exceptions for the Telegram Checklist Bot.

Defines custom exceptions used across the application. Using custom exceptions
allows the global error handling middleware to distinguish between expected
business logic errors and unexpected system crashes.
"""

class BotBaseException(Exception):
    """
    Base exception for all custom bot exceptions.
    
    All other custom exceptions should inherit from this class. It allows
    broad catching of known business-level errors without catching built-in
    Python exceptions like KeyError or ValueError.
    """
    pass

class ParserException(BotBaseException):
    """
    Exception raised for errors during the parsing phase.
    
    This is typically thrown by the ParserFactory if an unregistered parser
    is requested, or by individual parsers if they encounter malformed input
    that they are strictly unable to handle.
    """
    pass

class FormatterException(BotBaseException):
    """
    Exception raised for errors during the formatting phase.
    
    Thrown if a formatter is unable to handle a specific ParsedElement
    or encounters an unexpected state.
    """
    pass
