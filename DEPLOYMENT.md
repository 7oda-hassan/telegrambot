# Production Deployment Guide

This guide outlines the recommended steps for deploying the Telegram Rich Markdown Bot to a Linux Virtual Private Server (VPS) for long-term production execution.

## 1. Prerequisites

- A Linux-based VPS (Ubuntu 20.04/22.04 or Debian recommended).
- Root or `sudo` access.
- Python 3.11+ installed.
- Git.

## 2. Prepare the Environment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/telegram-rich-markdown-bot.git
   cd telegram-rich-markdown-bot
   ```

2. **Create a Virtual Environment:**
   It is highly recommended to isolate dependencies.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 3. Configuration

1. Create the environment variable file.
   ```bash
   cp .env.example .env
   ```
2. Securely edit `.env` using your preferred editor (e.g., `nano .env`) and set your required tokens.
   ```env
   BOT_TOKEN=123456789:YOUR_PRODUCTION_BOT_TOKEN_HERE
   ```

## 4. Process Management (Systemd)

To ensure the bot runs continuously, survives server reboots, and automatically restarts upon crashes, you must register it as a Systemd service.

1. **Create the Service File:**
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

2. **Paste the following configuration:**
   *(Ensure you replace `/path/to/project` and `your_user` with your actual directory and username)*
   ```ini
   [Unit]
   Description=Telegram Rich Markdown Bot
   After=network.target

   [Service]
   User=your_user
   Group=your_user
   WorkingDirectory=/path/to/project
   Environment="PATH=/path/to/project/venv/bin"
   ExecStart=/path/to/project/venv/bin/python main.py
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start the Service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   ```

## 5. Docker Deployment (Containerized)

If you prefer containerization, this repository includes a production-ready `Dockerfile` and `docker-compose.yml`.

### Using Docker Compose (Recommended)

This is the easiest and most reliable method to deploy the bot on any server.

1. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env and insert your BOT_TOKEN
   ```

2. **Start the Bot in the Background:**
   ```bash
   docker-compose up -d --build
   ```

3. **View Logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the Bot:**
   ```bash
   docker-compose down
   ```

### Using Raw Docker

If you aren't using `docker-compose`, you can build and run the image manually.

1. **Build the image:**
   ```bash
   docker build -t telegram-rich-bot .
   ```

2. **Run the container:**
   ```bash
   docker run -d --name rich-bot --env-file .env -v $(pwd)/logs:/app/logs telegram-rich-bot
   ```

## 6. Logging & Monitoring

The bot uses the native Python `logging` module configured for production environments. Errors and Warnings are piped directly to Standard Out, and rotating log files are saved to the `logs/` directory.

**To view live production logs (Systemd):**
```bash
sudo journalctl -u telegram-bot -f
```

**To restart the bot after code updates (Systemd):**
```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
```
