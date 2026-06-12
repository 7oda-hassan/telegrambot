# Architecture Documentation

The Telegram Rich Markdown Bot relies heavily on strict Clean Architecture paradigms. The core business logic (parsing, DOM building, and formatting) operates entirely decoupled from external frameworks (Aiogram/Telegram API). 

## 1. Request Flow (Message Processing)

When a message is received by Telegram, the flow travels from the outermost handler layer down into the core domain layer, and finally compiles back out to the Telegram API.

1. **Aiogram Dispatcher (`main.py`)**: Boots up the application and attaches routers and global error handling middlewares.
2. **Error Middleware (`error_middleware.py`)**: Intercepts the request. It traps exceptions, ensures users receive a graceful fallback message (`An unexpected system error occurred`), and strictly suppresses internal stack traces.
3. **Handler Layer (`checklist_handler.py`)**: Receives the raw Telegram API `Message` object. It contains zero parsing logic and delegates directly to the Application Service layer.
4. **Service Layer (`message_service.py`)**: Acts as the orchestrator. It receives the raw text and Telegram's native entities, invokes the parser, and forwards the AST to the formatter.
5. **API Layer (`send_rich_message.py`)**: Because `aiogram` does not currently expose the native `sendRichMessage` endpoint, a custom payload wrapper handles the transmission of the compiled markdown directly back to Telegram's backend.
   *(Note: The handler also includes an automatic fallback that seamlessly strips invalid embedded URLs if Telegram rejects the markdown payload due to `RICH_MESSAGE_PHOTO_URL_INVALID`).*

## 2. Parsing Pipeline

The parsing pipeline translates a flat Telegram message into a fully nested Abstract Syntax Tree (AST). The parser strictly prioritizes native Telegram Entities.

### A. Entity AST Builder (`entity_builder.py`)
This is the primary parser engine.
- Telegram's payloads deliver `entities` which use **UTF-16 Code Unit** offsets.
- The `EntityASTBuilder` rigidly decodes the raw text into a `utf-16-le` byte array, flawlessly slicing the byte strings using Telegram's exact bounds. This absolutely prevents "off-by-one" offset drifting caused by single-character multi-byte Emojis.
- The sliced boundaries are transformed directly into Semantic AST nodes (e.g. `BoldNode`, `InlineCodeNode`, `SpoilerNode`).

### B. Fallback Tokenizer (`tokenizer.py`)
For any unformatted plain text fragments scattered *between* the native Telegram entities, the `EntityASTBuilder` invokes the legacy state-machine `Tokenizer`.
- The Tokenizer leverages a `ParserRegistry` to invoke block-level plugins (`ChecklistPlugin`, `HeadingPlugin`).
- It strictly extracts block-level structures (such as `* [x] ` tasks) and translates them into semantic domain models (e.g. `TaskNode(completed=True)`).

## 3. Formatter Pipeline

### Telegram Rich Formatter (`telegram_rich_formatter.py`)
Once the complete, nested `DocumentNode` AST has been constructed, it is injected into the Formatter.

- The formatter implements a Visitor pattern (`_visit(node)`).
- It recursively traverses down the AST tree and complies each generic domain node (e.g., `TaskNode`) into the strict, proprietary GitHub-flavored Markdown required by the `sendRichMessage` Telegram endpoint.
- It automatically manages hard line breaks (enforcing `  \n` substitutions) to ensure multi-paragraph content does not syntactically collapse on Telegram mobile clients.

## 4. Expansion Paradigm

The Clean Architecture makes modifying or scaling features trivial:
- **Adding new Block elements**: Create a new plugin in `parsers/blocks/`, define the Regex pattern, and register it.
- **Adding new native Inline elements**: Inject the new Telegram `entity.type` check inside `entity_builder.py`.
- **Targeting new platforms**: Create an entirely new formatter (e.g., `DiscordFormatter` or `HTMLFormatter`) in `formatters/` and pass the identical AST tree into it. Zero parsers need to be refactored.
