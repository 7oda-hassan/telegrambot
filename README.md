# Telegram Rich Markdown Bot

A production-ready Telegram bot that processes custom Markdown elements, checklists, and text into Telegram's native Rich Formatting. Built with an extensible Abstract Syntax Tree (AST) architecture and a dynamic Role-Based User Interface.

## Key Features

- **Role-Based Dynamic UI**: The `/start` command automatically detects the user's role (Owner, Admin, User) and generates a dedicated interactive menu.
- **Markdown Session Mode**: Explicitly activate Markdown conversion via `/markdown` to prevent the bot from incorrectly parsing normal conversation messages.
- **Channel Publishing System**: Format messages using the Rich Markdown Engine and publish them seamlessly to connected Telegram channels.
- **Admin Management**: Securely delegate publishing permissions to other users without giving them full ownership.
- **Robust Error Handling**: Fails gracefully; no single user message can crash the bot.

## Available Roles & Permissions

- **Owner**: Full system access. Can add/remove admins, add/remove channels, format messages, and publish.
- **Admin**: Delegated access. Can format messages and publish them to any linked channel.
- **User**: General access. Can only convert markdown to preview Rich Messages.

## Deployment Environment Variables

This bot is fully configurable via Environment Variables. Never commit your secrets!

| Variable | Description | Required | Example |
|---|---|---|---|
| `BOT_TOKEN` | Your Telegram Bot API Token | **Yes** | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `OWNER_ID` | Your personal Telegram User ID | **Yes** | `123456789` |
| `LOG_LEVEL` | Python logging level (`INFO`, `DEBUG`, `ERROR`) | No | `INFO` |

## Local Setup

1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and fill in your details.
4. Run `python main.py`.

## Railway Deployment

This project is fully optimized for [Railway](https://railway.app/).
1. Link your GitHub repository in Railway.
2. Railway will automatically detect the Python environment and the `Procfile`.
3. Add `BOT_TOKEN` and `OWNER_ID` to the Railway **Variables** tab.
4. Deploy!
