"""
Abstract base parser definition.

This module provides the BaseParser interface that all concrete parsers must
implement, ensuring a consistent contract for extracting semantic elements
from plain text.
"""
from abc import ABC, abstractmethod
from typing import List
from parsers.models import ParsedElement

class BaseParser(ABC):
    """
    Abstract base class for all markdown parsers.
    
    Defines the standard `parse` method. By adhering to this interface,
    new parsers (e.g., BoldParser, LinkParser) can be integrated seamlessly
    into the ParserFactory without modifying consumer code.
    """

    @abstractmethod
    def parse(self, text: str) -> List[ParsedElement]:
        """
        Parses a block of text into a list of semantic elements.
        
        Args:
            text (str): The raw input text containing markdown or plain text.

        Returns:
            List[ParsedElement]: A list of objects inheriting from ParsedElement,
                                 representing the structured data found in the text.
        """
        pass
