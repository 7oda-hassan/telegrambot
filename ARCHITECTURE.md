# System Architecture

This project follows a strict **Clean Architecture** approach. It is heavily modularized to decouple the Telegram specific API layers from the core business logic, markdown parsing, and formatting engines.

## 1. Directory Structure

- `main.py`: The application entry point. Initializes databases, verifies environment variables, and starts polling.
- `bot/`: The Delivery mechanism (Controller layer).
  - `bot/handlers/`: Contains isolated command and event handlers (`session_handler`, `checklist_handler`, `menu_handler`, `channel_management_handler`, `publish_handler`).
  - `bot/middlewares/`: Security and error boundaries (`auth.py`, `error_middleware.py`).
  - `bot/services/`: Connects the Telegram handlers to the Database and external parsers.
- `parsers/`: The Core Business Logic for interpreting raw text.
  - Generates a modular Abstract Syntax Tree (AST) using plugins.
- `formatters/`: The Presentation Logic.
  - Converts the generated AST directly into Telegram's native formatting syntax.
- `core/`: Constants and base Exceptions.
- `data/`: Local storage for the SQLite database.

## 2. The Abstract Syntax Tree (AST) Pipeline

The bot's markdown capability is powered by a custom AST pipeline.

1. **Tokenization & Parsing (`parsers/`)**: The raw text message is broken down by the `ParserFactory` and `PluginLoader` into abstract mathematical nodes (e.g. `TaskNode`, `BoldNode`, `ParagraphNode`).
2. **Formatting (`formatters/`)**: The `TelegramRichMessageFormatter` traverses this tree of nodes recursively, appending the exact Markdown characters required by Telegram's `sendRichMessage` payload.
3. **Delivery (`bot/`)**: The formatted payload is dispatched back to the user via Aiogram.

This ensures that we never write "spaghetti code" string replacements. To add a new markdown feature, you simply create a new Node and add a tiny parsing plugin.

## 3. Session & Menu State

The application handles dynamic UI generation cleanly.

1. **Role Verification**: When a user types `/start`, the `session_handler` queries the Database (`ChannelService`) to determine if the user is an `OWNER`, `ADMIN`, or standard `USER`.
2. **Dynamic UI Generation**: Depending on the role, the bot builds a custom `InlineKeyboardMarkup` showing only the buttons the user is allowed to access.
3. **Session Toggling**: When the user clicks `Start Markdown Session` (or sends `/markdown`), a lightweight dictionary in `session_service.py` sets their `MARKDOWN_MODE` flag to `True`.
4. **Isolated Parsing**: The `checklist_handler.py` strictly drops all text messages *unless* the sender's `MARKDOWN_MODE` flag is `True`. Once one message is successfully processed, the flag is automatically switched back to `False`.

## 4. Error Isolation

Any exception thrown within a handler is intercepted by the `GlobalErrorMiddleware`. This ensures that a malformed message from a malicious or confused user only results in a localized error reply, keeping the main `Dispatcher` polling loop alive indefinitely.
