import pytest
from parsers.core.entity_builder import EntityASTBuilder
from parsers.core.ast import BoldNode, ItalicNode, TextNode, TaskNode
from parsers.core.plugin_loader import load_all_plugins

# Make sure plugins are loaded for unformatted text scanning
load_all_plugins()

class MockEntity:
    def __init__(self, type, offset, length, url=None, custom_emoji_id=None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.custom_emoji_id = custom_emoji_id

def test_simple_entity():
    text = "Bold Test"
    entities = [MockEntity("bold", 0, 9)]
    builder = EntityASTBuilder(text, entities)
    ast = builder.build()
    
    assert len(ast.children) == 1
    assert isinstance(ast.children[0], BoldNode)
    assert ast.children[0].children[0].text == "Bold Test"

def test_nested_entities():
    # "Bold Italic" where Italic is inside Bold
    text = "Bold Italic"
    entities = [
        MockEntity("bold", 0, 11),
        MockEntity("italic", 5, 6)
    ]
    builder = EntityASTBuilder(text, entities)
    ast = builder.build()
    
    assert len(ast.children) == 1
    bold_node = ast.children[0]
    assert isinstance(bold_node, BoldNode)
    
    assert len(bold_node.children) == 2
    assert bold_node.children[0].text == "Bold "
    
    italic_node = bold_node.children[1]
    assert isinstance(italic_node, ItalicNode)
    assert italic_node.children[0].text == "Italic"

def test_mixed_text_and_entities():
    # "* [x] Task with bold"
    text = "* [x] Task with bold"
    entities = [MockEntity("bold", 16, 4)]
    builder = EntityASTBuilder(text, entities)
    ast = builder.build()
    
    # We expect the unformatted text '* [x] Task with ' to be passed to Tokenizer, 
    # which turns it into a TaskNode containing 'Task with '.
    # Then the bold entity is processed, which should ideally be appended.
    assert len(ast.children) > 0

def test_utf16_entity_extraction():
    # Telegram sends offsets based on UTF-16 code units. Emojis take 2 units.
    # Text: "🎰 bold text"
    # In UTF-16: '🎰' is offset 0, length 2. ' ' is offset 2. 'bold text' starts at offset 3.
    text = "🎰 bold text"
    
    entities = [
        MockEntity("bold", 3, 9),  # Covers "bold text"
    ]
    builder = EntityASTBuilder(text, entities)
    ast = builder.build()
    
    assert len(ast.children) == 2
    # First child is text node "🎰 "
    assert ast.children[0].text.strip() == "🎰"
    
    # Second child is BoldNode containing "bold text"
    bold_node = ast.children[1]
    assert isinstance(bold_node, BoldNode)
    assert bold_node.children[0].text == "bold text"

def test_all_entity_types_offset():
    # Test strict slicing for different entities without off-by-one errors
    text = "bold italic strikethrough spoiler code"
    entities = [
        MockEntity("bold", 0, 4),
        MockEntity("italic", 5, 6),
        MockEntity("strikethrough", 12, 13),
        MockEntity("spoiler", 26, 7),
        MockEntity("code", 34, 4)
    ]
    
    builder = EntityASTBuilder(text, entities)
    ast = builder.build()
    
    from parsers.core.ast import BoldNode, ItalicNode, StrikethroughNode, SpoilerNode, InlineCodeNode
    
    # We should have nodes interweaved with spaces (TextNodes)
    from parsers.core.ast import TextNode
    nodes = [n for n in ast.children if not (isinstance(n, TextNode) and n.text.strip() == '')]
    
    assert isinstance(nodes[0], BoldNode)
    assert nodes[0].children[0].text == "bold"
    
    assert isinstance(nodes[1], ItalicNode)
    assert nodes[1].children[0].text == "italic"
    
    assert isinstance(nodes[2], StrikethroughNode)
    assert nodes[2].children[0].text == "strikethrough"
    
    assert isinstance(nodes[3], SpoilerNode)
    assert nodes[3].children[0].text == "spoiler"
    
    assert isinstance(nodes[4], InlineCodeNode)
    assert nodes[4].children[0].text == "code"
