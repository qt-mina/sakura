# GitHub Automation

This directory contains GitHub-specific configurations and automations for the Sakura bot.

## 📁 Structure

- `workflows/` - GitHub Actions workflow files for automated tasks

## 🔧 Workflows

### Bot Health Check & Auto-Redeploy

Automatically monitors the bot's health every 10 minutes. If the bot goes down, it triggers an automatic redeploy on Render.

**How it works:**
- Checks bot health via Telegram API every 10 minutes
- If bot responds (HTTP 200), sends a ✅ HEALTHY status message
- If bot doesn't respond, waits 30 seconds and rechecks
- If still down, automatically triggers redeploy on Render
- Sends detailed status notifications to your Telegram chat

**Schedule:**
- Runs at :00, :10, :20, :30, :40, :50 of every hour (6 times per hour)

**Notifications:**
- ✅ Healthy status every 10 minutes
- ❌ Down alerts with recovery attempts
- 🔄 Redeploy confirmations
- 🚨 Workflow error alerts

## 🔐 Secrets Required

The following secrets must be configured in GitHub repository settings:

- `BOT_TOKEN` - Your Telegram bot token
- `CHAT_ID` - Chat ID for status notifications (your personal chat or monitoring group)
- `REDEPLOY` - Render deploy hook URL for triggering redeployments

## 📊 Usage Limits

**Public Repositories:** Unlimited GitHub Actions minutes ✅

**Private Repositories:** 
- Free tier: 2,000 minutes/month
- Your usage: ~2,160 minutes/month (with 10-minute intervals)
- Consider making repository public or reducing check frequency if needed

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Deploy Hooks](https://render.com/docs/deploy-hooks)