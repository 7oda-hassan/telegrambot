# Installation Guide

Follow these steps to install and run the Telegram Rich Markdown Bot locally for development or manual execution. 
For production deployment via a VPS, please see [DEPLOYMENT.md](DEPLOYMENT.md).

## Prerequisites

- **Python**: Version 3.11 or newer is required.
- **Git**: To clone the repository.
- **Telegram Bot Token**: Obtain one by chatting with [@BotFather](https://t.me/BotFather) on Telegram.

## 1. Clone the Repository

```bash
git clone https://github.com/your-repo/telegram-rich-markdown-bot.git
cd telegram-rich-markdown-bot
```

## 2. Set Up a Virtual Environment

It is recommended to run the bot inside a Python virtual environment to prevent dependency conflicts.

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

Once the virtual environment is activated, install the required packages (such as `aiogram`, `python-dotenv`, and `pytest`):

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment Variables Configuration

The bot uses a `.env` file to securely manage secrets.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in a text editor and add your Bot Token:
   ```env
   BOT_TOKEN=123456789:YOUR_BOT_TOKEN_HERE
   ```

## 5. Running the Bot

To start the bot in development mode, run the `main.py` entry point:

```bash
python main.py
```

If configured correctly, the terminal will log `Starting Telegram Bot...` followed by `Bot is polling...`. The bot is now live and will respond to Checklist and Markdown inputs in your chats!
