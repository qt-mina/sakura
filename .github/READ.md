# GitHub Automation

This directory contains GitHub-specific configurations and automations for the Sakura bot.

## 📁 Structure

- `workflows/` - GitHub Actions workflow files for automated tasks

## 🔧 Workflows

### Bot Health Check & Auto-Redeploy

Automatically monitors the bot's health every 1 minute. If the bot goes down, it triggers an automatic redeploy on Render.

**How it works:**
- Sends a test message to your bot every minute
- If bot responds (HTTP 200), it's alive
- If bot doesn't respond, automatically triggers redeploy
- No messages sent to chat - silent health checks only

**Schedule:**
- Runs every 1 minute continuously

## 🔐 Secrets Required

The following secrets must be configured in GitHub repository settings:

- `BOT_TOKEN` - Your Telegram bot token
- `CHAT_ID` - Chat ID for health checks (can be your personal chat)
- `REDEPLOY` - Render deploy hook URL for triggering redeployments

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Deploy Hooks](https://render.com/docs/deploy-hooks)
