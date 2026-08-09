# Render deploy guide

## 1) Prepare the project
Make sure these files are in the repository root:
- main.py
- requirements.txt
- render.yaml
- Procfile
- .env.example

## 2) Create a GitHub repository
If the project is not already in GitHub:

```bash
git init
git branch -M main
git add .
git commit -m "Initial bot deployment"
```

Then create a repository on GitHub and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## 3) Add the bot token in Render
In Render, create a Web Service from the GitHub repo.

Use these values:
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`

Environment variables:
- `BOT_TOKEN`: your Telegram bot token
- `ADMIN_ID`: your Telegram chat ID (optional)

## 4) Verify the bot
After deployment:
1. Open the Render service logs.
2. Confirm the bot starts successfully.
3. Open Telegram and send `/start` to the bot.

## 5) If the bot does not respond
Check the Render logs for:
- missing token
- import errors
- polling conflicts

If needed, restart the service from the Render dashboard.
