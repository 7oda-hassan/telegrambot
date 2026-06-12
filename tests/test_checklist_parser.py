import pytest
from parsers.core.tokenizer import Tokenizer, ASTBuilder
from parsers.core.plugin_loader import load_all_plugins
from parsers.core.ast import TaskNode, TextNode, DocumentNode

# Ensure plugins are loaded for tests
load_all_plugins()

def test_checked_item():
    text = "* [x] Learn Markdown basics"
    tokenizer = Tokenizer(text)
    ast = ASTBuilder(tokenizer.tokenize()).build()
    
    assert len(ast.children) == 1
    assert isinstance(ast.children[0], TaskNode)
    assert ast.children[0].completed is True
    assert ast.children[0].children[0].text == "Learn Markdown basics"

def test_unchecked_item():
    text = "* [ ] Apply ready templates"
    tokenizer = Tokenizer(text)
    ast = ASTBuilder(tokenizer.tokenize()).build()
    
    assert len(ast.children) == 1
    assert isinstance(ast.children[0], TaskNode)
    assert ast.children[0].completed is False
    assert ast.children[0].children[0].text == "Apply ready templates"

def test_mixed_list():
    text = "* [x] Task 1\n* [ ] Task 2"
    tokenizer = Tokenizer(text)
    ast = ASTBuilder(tokenizer.tokenize()).build()
    
    # Task 1, Newline, Task 2
    assert isinstance(ast.children[0], TaskNode)
    assert ast.children[0].completed is True
    assert isinstance(ast.children[1], TextNode)
    assert ast.children[1].text == "\n"
    assert isinstance(ast.children[2], TaskNode)
    assert ast.children[2].completed is False
