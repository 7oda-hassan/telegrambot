from typing import Optional, Tuple
from parsers.core.tokenizer import Token, BasePlugin, ASTBuilder, ParserRegistry
from parsers.core.ast import TaskNode

class ChecklistPlugin(BasePlugin):
    priority = 90

    def tokenize(self, text: str, pos: int) -> Optional[Tuple[Token, int]]:
        if pos == 0 or text[pos - 1] == '\n':
            if text.startswith("- [x] ", pos) or text.startswith("* [x] ", pos):
                return Token("TASK_CHECKED", text[pos:pos+6]), pos + 6
            elif text.startswith("- [X] ", pos) or text.startswith("* [X] ", pos):
                return Token("TASK_CHECKED", text[pos:pos+6]), pos + 6
            elif text.startswith("- [ ] ", pos) or text.startswith("* [ ] ", pos):
                return Token("TASK_UNCHECKED", text[pos:pos+6]), pos + 6
        return None

    def build(self, builder: ASTBuilder, token: Token) -> bool:
        if token.type in ("TASK_CHECKED", "TASK_UNCHECKED"):
            node = TaskNode(completed=(token.type == "TASK_CHECKED"))
            builder.current_parent().children.append(node)
            builder.stack.append(node)
            return True
        return False

ParserRegistry.register(ChecklistPlugin)
