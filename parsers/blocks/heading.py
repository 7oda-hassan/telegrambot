from typing import Optional, Tuple
from parsers.core.tokenizer import Token, BasePlugin, ASTBuilder, ParserRegistry
from parsers.core.ast import HeadingNode

class HeadingPlugin(BasePlugin):
    priority = 80

    def tokenize(self, text: str, pos: int) -> Optional[Tuple[Token, int]]:
        if pos == 0 or text[pos - 1] == '\n':
            if text.startswith("# ", pos):
                return Token("HEADING", "# "), pos + 2
            elif text.startswith("## ", pos):
                return Token("HEADING", "## "), pos + 3
            elif text.startswith("### ", pos):
                return Token("HEADING", "### "), pos + 4
        return None

    def build(self, builder: ASTBuilder, token: Token) -> bool:
        if token.type == "HEADING":
            level = token.value.count('#')
            node = HeadingNode(level=level)
            builder.current_parent().children.append(node)
            builder.stack.append(node)
            return True
        return False

ParserRegistry.register(HeadingPlugin)
