"""
Core tokenizer engine for Markdown block parsing.

This module consolidates the Token, BasePlugin interface, ParserRegistry,
Tokenizer, and ASTBuilder into a single tightly-coupled module to reduce
overhead. It falls back to tokenizing unformatted blocks (like Checklists).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Type

from parsers.core.ast import (
    DocumentNode, TextNode, HeadingNode, TaskNode, ParentNode
)

@dataclass
class Token:
    type: str
    value: str

class BasePlugin(ABC):
    """
    Abstract base class for all Markdown block parsers.
    """
    priority: int = 100

    @abstractmethod
    def tokenize(self, text: str, pos: int) -> Optional[Tuple[Token, int]]:
        pass

    @abstractmethod
    def build(self, builder: 'ASTBuilder', token: Token) -> bool:
        pass

class ParserRegistry:
    """
    Global registry for Markdown parser plugins.
    """
    _plugins: List[BasePlugin] = []

    @classmethod
    def register(cls, plugin_class: Type[BasePlugin]):
        plugin_instance = plugin_class()
        cls._plugins.append(plugin_instance)
        cls._plugins.sort(key=lambda p: p.priority, reverse=True)

    @classmethod
    def get_plugins(cls) -> List[BasePlugin]:
        return cls._plugins

class Tokenizer:
    """
    Character-by-character state-machine scanner for unformatted blocks.
    """
    def __init__(self, text: str):
        self.text = text
        self.length = len(text)
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        pos = 0
        plugins = ParserRegistry.get_plugins()
        
        while pos < self.length:
            matched = False
            for plugin in plugins:
                result = plugin.tokenize(self.text, pos)
                if result:
                    token, new_pos = result
                    if token:
                        self.tokens.append(token)
                    pos = new_pos
                    matched = True
                    break
            
            if not matched:
                char = self.text[pos]
                if char == '\n':
                    self.tokens.append(Token("NEWLINE", "\n"))
                else:
                    self.tokens.append(Token("TEXT", char))
                pos += 1
                
        # Consolidate consecutive TEXT tokens
        final_tokens = []
        text_buffer = ""
        for t in self.tokens:
            if t.type == "TEXT":
                text_buffer += t.value
            else:
                if text_buffer:
                    final_tokens.append(Token("TEXT", text_buffer))
                    text_buffer = ""
                final_tokens.append(t)
        if text_buffer:
            final_tokens.append(Token("TEXT", text_buffer))
            
        return final_tokens

class ASTBuilder:
    """
    Consumes tokens and builds the Abstract Syntax Tree for unformatted blocks.
    """
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)
        self.root = DocumentNode()
        self.stack: List[ParentNode] = [self.root]

    def current_parent(self) -> ParentNode:
        return self.stack[-1]

    def build(self) -> DocumentNode:
        plugins = ParserRegistry.get_plugins()
        while self.pos < self.length:
            tok = self.tokens[self.pos]
            self.pos += 1

            matched = False
            for plugin in plugins:
                if plugin.build(self, tok):
                    matched = True
                    break
            
            if not matched:
                if tok.type == "TEXT":
                    self.current_parent().children.append(TextNode(text=tok.value))
                elif tok.type == "NEWLINE":
                    if isinstance(self.current_parent(), (HeadingNode, TaskNode)):
                        self.stack.pop()
                    self.current_parent().children.append(TextNode(text="\n"))

        return self.root
