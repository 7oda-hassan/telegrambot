"""
Domain models for the parsing layer.

Defines the semantic data structures (dataclasses) that represent parsed
elements of a message. These models form the contract between the Parser layer
(which produces them) and the Formatter layer (which consumes them).
"""
from dataclasses import dataclass

@dataclass
class ParsedElement:
    """
    Abstract base class for all parsed elements.
    
    Serves as the root type for elements extracted from user input.
    """
    pass

@dataclass
class TextElement(ParsedElement):
    """
    Represents raw, unformatted text or text that didn't match any specific parser.
    
    Attributes:
        text (str): The raw string content.
    """
    text: str

@dataclass
class Task(ParsedElement):
    """
    Represents a successfully parsed checklist item (task).
    
    Attributes:
        text (str): The text content of the task (excluding the markdown bullet/checkbox).
        completed (bool): True if the task was marked as [x] or [X], False if [ ].
    """
    text: str
    completed: bool
