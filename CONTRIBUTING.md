# Contributing

We welcome contributions to the Telegram Rich Markdown Bot!

## Clean Architecture Requirements

This project adheres strictly to **Clean Architecture**. If you are adding a new feature, please follow these guidelines:

1. **Domain Layer Independence**: Business logic, including AST Node definitions (`parsers/core/ast.py`), must not depend on the Telegram API or the `aiogram` framework.
2. **Entity Slicing**: If you are adding support for a new native Telegram Entity type, do **not** use Regex fallback parsers. Implement it natively via `EntityASTBuilder` in `parsers/core/entity_builder.py`.
3. **Formatters**: The `formatters` directory exclusively compiles AST Nodes into raw output strings. Formatters must never mutate the domain models.

## Development Workflow

1. Fork the repository and clone it to your local machine.
2. Create a virtual environment (`python -m venv venv`) and activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a new branch for your feature (`git checkout -b feature/your-feature`).
5. Ensure all Pytest test suites continue to pass:
   ```bash
   pytest tests/
   ```
6. Commit your changes and push to your fork.
7. Submit a Pull Request with a clear description of the new architecture additions.

## Testing Guidelines
- All changes to `EntityASTBuilder` offset slicing must include rigorous unit tests containing **multi-byte emojis** to guarantee that UTF-16 offset drift regressions are not introduced.
