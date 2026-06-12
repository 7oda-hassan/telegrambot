"""
Concrete parser implementation for Markdown checklists.

This module contains the logic to identify and extract Markdown checklist items
while preserving surrounding plain text and line breaks.
"""
from typing import List
from core.constants import CHECKLIST_REGEX
from parsers.base_parser import BaseParser
from parsers.models import ParsedElement, Task, TextElement

class ChecklistParser(BaseParser):
    """
    Parser specifically designed for Markdown checklists.
    
    It scans the input text line-by-line. If a line matches the Markdown
    checklist syntax (e.g., `* [x] Task`), it is converted into a `Task`.
    Otherwise, the line is preserved exactly as a `TextElement`, including
    empty lines.
    """

    def parse(self, text: str) -> List[ParsedElement]:
        """
        Parses text to extract checklist items.
        
        Args:
            text (str): The raw user input message.
            
        Returns:
            List[ParsedElement]: A list of TextElement and Task objects.
                                 The order strictly follows the input text line order.
        """
        if not text:
            return []

        elements: List[ParsedElement] = []
        lines = text.splitlines()

        for line in lines:
            if not line.strip():
                # Preserve empty lines as empty text elements to maintain spacing
                elements.append(TextElement(text=""))
                continue

            match = CHECKLIST_REGEX.match(line.strip())
            if match:
                # Extract the status character ('x', 'X', or ' ')
                status_char = match.group("status").strip().lower()
                completed = status_char == "x"
                
                # Extract the task description text
                item_text = match.group("text")
                elements.append(Task(text=item_text, completed=completed))
            else:
                # If the line isn't a checklist, keep it exactly as it is
                elements.append(TextElement(text=line))
                
        return elements
