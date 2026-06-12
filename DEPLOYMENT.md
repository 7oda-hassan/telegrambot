# Deployment Guide

This document explains how to securely deploy the Telegram Rich Markdown Bot to production environments, specifically focusing on cloud PaaS providers like **Railway** and traditional VPS environments using **Docker**.

## 1. Environment Configuration

All sensitive configurations must be injected via Environment Variables.

Create a `.env` file or provide these variables in your deployment dashboard:

```env
BOT_TOKEN=123456789:YOUR_SECRET_TOKEN
OWNER_ID=123456789
LOG_LEVEL=INFO
```

*Note: The bot will fail fast and exit immediately on startup if `BOT_TOKEN` or `OWNER_ID` are missing or improperly formatted.*

---

## 2. Railway Deployment (Recommended)

Railway is the easiest way to deploy this bot, as the repository is pre-configured with a `Procfile` and standard Python packaging.

1. Create a Railway account and link your GitHub account.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will begin building. It will likely fail initially because of missing variables.
5. Go to the **Variables** tab in your Railway project.
6. Add `BOT_TOKEN` and `OWNER_ID`.
7. Railway will automatically redeploy the bot.
8. Check the **Logs** tab. You should see `Starting Telegram Bot...` followed by `Bot is polling...`.

---

## 3. Docker Compose Deployment (VPS / Self-Hosted)

If you are hosting this on a Linux VPS (e.g. DigitalOcean, Linode, AWS EC2), you can use the provided Docker setup.

1. Ensure Docker and Docker Compose are installed on your server.
2. Clone the repository:
   ```bash
   git clone https://github.com/your-username/telegrambot.git
   cd telegrambot
   ```
3. Copy the environment template:
   ```bash
   cp .env.example .env
   nano .env # Insert your BOT_TOKEN and OWNER_ID
   ```
4. Build and start the container in the background:
   ```bash
   docker-compose up -d --build
   ```
5. View logs to confirm startup:
   ```bash
   docker-compose logs -f
   ```

---

## 4. Production Database Strategy

The bot utilizes a lightweight `SQLite3` database to store Channels, Admins, and Drafts. 
The database is automatically generated inside the `data/` directory (`data/bot_database.sqlite`). 

**Important Note for PaaS (Railway/Heroku):**
If you deploy to a serverless or ephemeral file system, the SQLite database might reset between redeployments. For Railway, ensure you attach a **Volume** to the `/app/data` directory inside the service settings to make the database persistent!
