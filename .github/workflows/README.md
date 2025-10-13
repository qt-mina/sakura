# Workflow Automations

This directory contains GitHub Actions workflows for automating Sakura bot operations.

## 📋 Available Workflows

### `health-check.yml` - Bot Health Check & Auto-Redeploy

Automatically monitors the bot's health and redeploys if it goes down.

**Purpose:**
- Detects bot crashes immediately
- Automatically redeploys on Render when bot is down
- Ensures 24/7 uptime with minimal downtime
- Silent health checks (no chat messages)

**Schedule:**
- Runs every 1 minute continuously
- Checks if bot is responsive via Telegram API
- Triggers redeploy only when bot is detected as down

**Manual Trigger:**
You can manually trigger this workflow:
1. Go to Actions tab
2. Select "Bot Health Check & Auto-Redeploy"
3. Click "Run workflow"
4. Click the green "Run workflow" button

## 🔧 Configuration

### Required Secrets

- **BOT_TOKEN**: Your Telegram bot token
  - Format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
  - Get from: [@BotFather](https://t.me/botfather) on Telegram

- **CHAT_ID**: Chat ID for health check messages
  - Format: A number (e.g., `987654321`)
  - Can be your personal chat ID or a test group
  - Get from: Send a message to your bot and check the update

- **REDEPLOY**: Render deploy hook URL
  - Get from: Render Dashboard → Service → Settings → Deploy Hook
  - Format: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`

### Modifying Check Frequency

To change how often the bot is checked, edit the `cron` value in `redeploy.yml`:

```yaml
# Every 1 minute (current)
cron: '* * * * *'

# Every 5 minutes
cron: '*/5 * * * *'

# Every 10 minutes
cron: '*/10 * * * *'

# Every 30 minutes
cron: '*/30 * * * *'
```

## 📊 Monitoring

### Check Workflow Status
1. Go to the **Actions** tab in your repository
2. Click on "Bot Health Check & Auto-Redeploy"
3. View recent runs and their status
4. Click on a run to see detailed logs

### Verify Bot Health
1. Open your bot's chat
2. Send a test command to verify it's responding
3. Check workflow runs - if no recent redeployments, bot is healthy

### Monitor Render Deployments
1. Open Render Dashboard
2. Go to your service
3. Check the **Events** or **Logs** tab
4. Look for "Deploy hook" triggered deployments

## 🐛 Troubleshooting

### Workflow Not Running
- Check if Actions are enabled in repository settings
- Verify the workflow file exists in `.github/workflows/redeploy.yml`
- Ensure the workflow has proper YAML formatting

### Frequent Redeployments
- Your bot may be crashing repeatedly
- Check Render logs for errors
- Verify bot code for memory leaks or infinite loops
- Consider increasing check interval (e.g., every 5 minutes instead of 1)

### Wrong Chat ID
- Health check will fail if CHAT_ID is invalid
- Get correct chat ID: send any message to your bot, check the update
- Test by sending a message to your bot manually

### Redeploy Not Triggering
- Verify the `REDEPLOY` secret contains the correct Render deploy hook URL
- Check if Render service is still active
- Review workflow logs in Actions tab for error messages

## 📝 Notes

- GitHub Actions cron jobs may have a 3-15 minute delay during high traffic
- Health checks are silent - no visible messages in your chat
- The workflow runs on GitHub servers, independent of your bot's status
- Even if Render shuts down your free instance, the workflow will detect it and redeploy
- First health check after bot startup may fail (allow 10-30 seconds for bot to initialize)
