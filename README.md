# Telegram Rich Markdown Bot

## Project Overview

The Telegram Rich Markdown Bot is a high-performance Python application designed to natively parse and render advanced formatting within the Telegram ecosystem. Built on `aiogram` and Clean Architecture principles, this bot leverages Telegram's bleeding-edge `sendRichMessage` API to render pristine interactive block-level and inline elements—such as interactive checklists, code blocks, and formatting—exactly as they appear in the official native clients.

Main use cases include:
- Processing interactive Checklists.
- Formatting cleanly organized Markdown messages for channels and groups.
- Displaying beautifully aligned multi-line code blocks and structured tables.

## Supported Features

The bot fully parses and perfectly reconstructs the following Telegram native features without resorting to brittle HTML parsing:

- **Headings** (H1 - H6)
- **Checklists** (Interactive native Task Lists)
- **Block Quotes**
- **Code Blocks** (Triple backticks with language tags)
- **Inline Code** (Single backticks)
- **Bold** 
- **Italic**
- **Strikethrough**
- **Spoilers**
- **Links & Inline Links**
- **Custom Emoji**
- **Mentions**
- **Email Links**
- **Phone Links**

*Note: Features like Math and Tables are processed natively if correctly formed by the client payload. If media/photo URLs are invalid, the bot intelligently falls back to text rendering without dropping messages.*

## Installation

### Prerequisites
- Python 3.11+
- A valid Telegram Bot API token from [@BotFather](https://t.me/BotFather)

### Environment Setup

1. **Clone the repository** and navigate into the root directory.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your bot token:
   ```env
   BOT_TOKEN=123456789:YOUR_BOT_TOKEN_HERE
   ```

## Running The Bot

### Local Execution (Development)
For local testing or development, you can run the bot directly via Python:
```bash
python main.py
```

### Docker Compose (Production)
The most reliable way to execute the bot in a production environment is via Docker.
```bash
docker-compose up -d --build
```
You can view the logs seamlessly using:
```bash
docker-compose logs -f
```

### Linux VPS / Systemd (Production)
For bare-metal deployments on Ubuntu/Debian servers without Docker, please consult the explicit commands and service configurations outlined in [DEPLOYMENT.md](DEPLOYMENT.md).

## Project Structure

The project is structured following strict Clean Architecture principles, ensuring that parsing business logic is entirely decoupled from the Telegram API handler layer.

```text
├── .env
├── requirements.txt
├── main.py
├── bot/
│   ├── api/                 # Custom Aiogram bindings (SendRichMessage)
│   ├── handlers/            # Aiogram message controllers
│   ├── middlewares/         # Global Error handling
│   └── services/            # Domain use-case orchestrators
├── formatters/              # Markdown AST-to-Telegram syntax compilers
├── parsers/
│   ├── core/                # Core parsing engines (EntityASTBuilder, Tokenizer, AST)
│   ├── blocks/              # Block-level parser plugins (Headings)
│   └── lists/               # List-level parser plugins (Checklists)
├── tests/                   # Pytest automated test suites
└── utils/
    └── logger.py            # Global production logging configuration
```
