"""
Factory for managing parser instantiations.

Provides a centralized registry to create parsers dynamically by name.
This supports the Open/Closed Principle: the system is open for extension
(registering new parsers) but closed for modification (consumer code doesn't
need to import concrete parser classes directly).
"""
from typing import Type, Dict
from parsers.base_parser import BaseParser
from parsers.checklist_parser import ChecklistParser
from core.exceptions import ParserException

class ParserFactory:
    """
    Factory class for creating and managing BaseParser implementations.
    
    Contains a dictionary of pre-registered parsers and provides a
    classmethod to retrieve instances. New parsers can be added via `register_parser`.
    """
    
    _parsers: Dict[str, Type[BaseParser]] = {
        "checklist": ChecklistParser
    }

    @classmethod
    def get_parser(cls, parser_name: str) -> BaseParser:
        """
        Retrieves an instance of a parser by its registered name.
        
        Args:
            parser_name (str): The key name of the registered parser (e.g., 'checklist').
            
        Returns:
            BaseParser: An instance of the requested parser class.
            
        Raises:
            ParserException: If the requested parser_name does not exist in the registry.
        """
        parser_class = cls._parsers.get(parser_name)
        if not parser_class:
            raise ParserException(f"Parser '{parser_name}' is not registered.")
        return parser_class()

    @classmethod
    def register_parser(cls, parser_name: str, parser_class: Type[BaseParser]) -> None:
        """
        Registers a new parser class into the factory.
        
        Args:
            parser_name (str): The name to associate with the parser.
            parser_class (Type[BaseParser]): The uninstantiated class inheriting from BaseParser.
        """
        cls._parsers[parser_name] = parser_class
