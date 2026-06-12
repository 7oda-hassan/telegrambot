import pytest
from formatters.telegram_rich_formatter import TelegramRichMessageFormatter
from parsers.core.ast import DocumentNode, TaskNode, TextNode, BoldNode

def test_telegram_rich_formatter():
    formatter = TelegramRichMessageFormatter()
    
    task1 = TaskNode(completed=True)
    task1.children.append(TextNode("Task 1 "))
    bold = BoldNode()
    bold.children.append(TextNode("bold"))
    task1.children.append(bold)
    
    task2 = TaskNode(completed=False)
    task2.children.append(TextNode("Task 2"))
    
    doc = DocumentNode(children=[task1, TextNode("\n"), task2])
    result = formatter.format(doc)
    
    assert result == "* [x] Task 1 **bold**  \n* [ ] Task 2"
