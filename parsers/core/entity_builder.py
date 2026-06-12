from typing import List, Optional, Any
from parsers.core.ast import (
    ASTNode, DocumentNode, TextNode, BoldNode, ItalicNode, 
    StrikethroughNode, SpoilerNode, UnderlineNode, 
    TextLinkNode, CustomEmojiNode, ParentNode
)
from parsers.core.tokenizer import Tokenizer, ASTBuilder

class EntityASTBuilder:
    """
    Constructs an AST by mapping Telegram's pre-parsed MessageEntity objects.
    Any text not covered by an entity is delegated to the legacy Tokenizer 
    to capture block-level elements like Checklists or Headings.
    """
    def __init__(self, text: str, entities: List[Any]):
        self.text = text
        self.text_utf16 = text.encode("utf-16-le")
        # Ensure entities are sorted by offset, then by length descending (outermost first)
        self.entities = sorted(entities, key=lambda e: (e.offset, -e.length)) if entities else []

    def _slice_text(self, start: int, end: int) -> str:
        """Extract text using UTF-16 code unit offsets exactly as provided by Telegram."""
        if start >= end:
            return ""
        try:
            return self.text_utf16[start * 2 : end * 2].decode("utf-16-le")
        except UnicodeDecodeError:
            return ""

    def build(self) -> DocumentNode:
        root = DocumentNode()
        self._process_range(root, 0, len(self.text_utf16) // 2, self.entities)
        return root

    def _process_range(self, parent: ParentNode, start: int, end: int, entities: List[Any]):
        current_pos = start
        
        # Filter entities that strictly belong within this range
        range_entities = [e for e in entities if e.offset >= start and (e.offset + e.length) <= end]
        
        # Find outermost entities (those not contained within another entity in the current list)
        outer_entities = []
        last_end = -1
        for e in range_entities:
            # Because they are sorted by offset (and length desc), an entity is nested 
            # if its offset is within the bounds of the last outermost entity.
            if e.offset >= last_end:
                outer_entities.append(e)
                last_end = e.offset + e.length

        for entity in outer_entities:
            # 1. Process unformatted text BEFORE this entity
            if current_pos < entity.offset:
                self._parse_unformatted_text(parent, self._slice_text(current_pos, entity.offset))
                
            # 2. Create the semantic node for this entity
            node = self._create_node_from_entity(entity)
            parent.children.append(node)
            
            # 3. Recursively process nested entities INSIDE this entity
            entity_end = entity.offset + entity.length
            nested_entities = [e for e in range_entities if e != entity and e.offset >= entity.offset and (e.offset + e.length) <= entity_end]
            
            # If the node can have children, process them. Otherwise it's just raw text.
            if isinstance(node, ParentNode):
                if not nested_entities:
                    # If there are no nested entities, the internal content is unformatted
                    self._parse_unformatted_text(node, self._slice_text(entity.offset, entity_end))
                else:
                    self._process_range(node, entity.offset, entity_end, nested_entities)

            current_pos = entity_end

        # 4. Process any remaining unformatted text AFTER the last entity
        if current_pos < end:
            self._parse_unformatted_text(parent, self._slice_text(current_pos, end))

    def _parse_unformatted_text(self, parent: ParentNode, text: str):
        """Passes unformatted text to the base tokenizer to capture block syntax like checklists."""
        if not text:
            return
            
        tokenizer = Tokenizer(text)
        tokens = tokenizer.tokenize()
        builder = ASTBuilder(tokens)
        doc = builder.build()
        
        # Append all parsed elements (Tasks, Headings, or plain Text) to the parent
        parent.children.extend(doc.children)

    def _create_node_from_entity(self, entity: Any) -> ASTNode:
        t = entity.type
        if t == "bold":
            return BoldNode()
        elif t == "italic":
            return ItalicNode()
        elif t == "strikethrough":
            return StrikethroughNode()
        elif t == "spoiler":
            return SpoilerNode()
        elif t == "underline":
            return UnderlineNode()
        elif t == "text_link":
            return TextLinkNode(url=getattr(entity, "url", ""))
        elif t == "custom_emoji":
            return CustomEmojiNode(custom_emoji_id=getattr(entity, "custom_emoji_id", ""))
        elif t == "code":
            # Code is an inline code block.
            from parsers.core.ast import InlineCodeNode
            return InlineCodeNode()
        elif t == "pre":
            from parsers.core.ast import CodeBlockNode
            return CodeBlockNode(language=getattr(entity, "language", ""))
        else:
            # Fallback for unsupported entities
            return ParentNode()
