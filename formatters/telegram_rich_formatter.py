"""
Formatter for Telegram Rich Messages.

This module is responsible for traversing the constructed AST 
and converting it into the final Markdown syntax required by Telegram's
native sendRichMessage API.
"""

from parsers.core.ast import (
    ASTNode, DocumentNode, ParagraphNode, TextNode, 
    BoldNode, ItalicNode, StrikethroughNode, SpoilerNode, 
    TaskNode, HeadingNode, ParentNode,
    UnderlineNode, TextLinkNode, CustomEmojiNode, CodeBlockNode, InlineCodeNode
)

class TelegramRichMessageFormatter:
    """
    Traverses the generated AST and compiles it into raw Markdown.
    """

    def format(self, node: ASTNode) -> str:
        """
        Converts an ASTNode into a final formatted string.
        """
        return self._visit(node)

    def _visit(self, node: ASTNode) -> str:
        if isinstance(node, TextNode):
            # Telegram's standard markdown parser collapses single/double newlines.
            # Appending two spaces forces a hard line break in standard Markdown.
            return node.text.replace("\n", "  \n")

        if isinstance(node, ParentNode):
            children_str = "".join(self._visit(child) for child in node.children)
            
            # Prevent rendering empty markup tags
            if not children_str and not isinstance(node, DocumentNode):
                return ""
                
            if isinstance(node, DocumentNode):
                return children_str
            elif isinstance(node, BoldNode):
                return f"**{children_str}**"
            elif isinstance(node, ItalicNode):
                return f"*{children_str}*"
            elif isinstance(node, StrikethroughNode):
                return f"~~{children_str}~~"
            elif isinstance(node, SpoilerNode):
                return f"||{children_str}||"
            elif isinstance(node, UnderlineNode):
                return f"__{children_str}__"
            elif isinstance(node, TextLinkNode):
                return f"[{children_str}]({node.url})"
            elif isinstance(node, CustomEmojiNode):
                return f"![{children_str}](tg://emoji?id={node.custom_emoji_id})"
            elif isinstance(node, InlineCodeNode):
                return f"`{children_str}`"
            elif isinstance(node, CodeBlockNode):
                lang = node.language if node.language else ""
                return f"```{lang}\n{children_str}\n```"
            elif isinstance(node, HeadingNode):
                prefix = "#" * node.level
                return f"{prefix} {children_str}"
            elif isinstance(node, TaskNode):
                mark = "x" if node.completed else " "
                return f"* [{mark}] {children_str}"
            elif isinstance(node, ParagraphNode):
                return f"{children_str}\n\n"
            else:
                return children_str

        return ""
