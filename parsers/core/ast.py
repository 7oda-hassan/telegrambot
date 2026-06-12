from dataclasses import dataclass, field
from typing import List

@dataclass
class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    pass

@dataclass
class ParentNode(ASTNode):
    """A node that can contain other nodes (e.g., Bold, Paragraph)."""
    children: List[ASTNode] = field(default_factory=list)

@dataclass
class TextNode(ASTNode):
    """A raw text node."""
    text: str

# --- Inline Nodes ---
@dataclass
class BoldNode(ParentNode):
    pass

@dataclass
class ItalicNode(ParentNode):
    pass

@dataclass
class StrikethroughNode(ParentNode):
    pass

@dataclass
class SpoilerNode(ParentNode):
    pass

@dataclass
class UnderlineNode(ParentNode):
    pass

@dataclass
class TextLinkNode(ParentNode):
    url: str = ""

@dataclass
class CustomEmojiNode(ParentNode):
    custom_emoji_id: str = ""

@dataclass
class InlineCodeNode(ParentNode):
    type: str = "inline_code"

@dataclass
class CodeBlockNode(ParentNode):
    language: str = ""
class ParagraphNode(ParentNode):
    pass

@dataclass
class HeadingNode(ParentNode):
    level: int = 1

# --- List Nodes ---
@dataclass
class TaskNode(ParentNode):
    completed: bool = False

@dataclass
class DocumentNode(ParentNode):
    pass
