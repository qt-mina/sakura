# Workflow Automations

This directory contains GitHub Actions workflows for automating Sakura bot operations.

## 📋 Available Workflows

### `redeploy.yml` - Bot Health Check & Auto-Redeploy

Automatically monitors the bot's health and redeploys if it goes down.

**Purpose:**
- Detects bot crashes immediately
- Automatically redeploys on Render when bot is down
- Ensures 24/7 uptime with minimal downtime
- Sends detailed status notifications to Telegram

**Schedule:**
- Runs every 10 minutes (at :00, :10, :20, :30, :40, :50 of each hour)
- Checks if bot is responsive via Telegram API
- Double-checks before redeploying (waits 30 seconds and rechecks)
- Only triggers redeploy when bot is confirmed down

**Notifications:**
- ✅ **HEALTHY** - Bot is working fine (every 10 minutes)
- ❌ **DOWN** - Bot failed health check, initiating recovery
- ✅ **RECOVERED** - Bot came back online during recheck
- 🔄 **REDEPLOY TRIGGERED** - Automatic redeploy initiated
- 🚨 **WORKFLOW ERROR** - GitHub Actions workflow failed

**Manual Trigger:**
You can manually trigger this workflow:
1. Go to Actions tab
2. Select "Bot Health Check & Auto-Redeploy"
3. Click "Run workflow"
4. Click the green "Run workflow" button

## 🔧 Configuration

### Required Secrets

Configure these in: **Repository Settings → Secrets and variables → Actions → New repository secret**

- **BOT_TOKEN**: Your Telegram bot token
  - Format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`
  - Get from: [@BotFather](https://t.me/botfather) on Telegram

- **CHAT_ID**: Chat ID for health check messages
  - Format: A number (e.g., `987654321` or `-1001234567890` for groups)
  - Can be your personal chat ID or a monitoring group
  - Get from: Send `/start` to [@userinfobot](https://t.me/userinfobot) on Telegram

- **REDEPLOY**: Render deploy hook URL
  - Get from: Render Dashboard → Your Service → Settings → Deploy Hook
  - Format: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`

### Modifying Check Frequency

To change how often the bot is checked, edit the `cron` value in `redeploy.yml`:

```yaml
# Every 10 minutes (current - recommended)
cron: '0,10,20,30,40,50 * * * *'

# Every 15 minutes (uses ~1,440 minutes/month)
cron: '0,15,30,45 * * * *'

# Every 20 minutes (uses ~1,080 minutes/month)
cron: '0,20,40 * * * *'

# Every 30 minutes (uses ~720 minutes/month)
cron: '0,30 * * * *'
```

**Note:** Using the format `0,10,20,30,40,50` instead of `*/10` is more reliable with GitHub Actions cron scheduler.

### Silencing Healthy Notifications

If you find the ✅ HEALTHY messages too frequent, modify the "Send status update" step in `redeploy.yml`:

```yaml
- name: Send status update
  if: steps.health.outputs.status == 'down'  # Only notify when down
  run: |
    curl -s -X POST "https://api.telegram.org/bot${{ secrets.BOT_TOKEN }}/sendMessage" \
      -d "chat_id=${{ secrets.CHAT_ID }}" \
      -d "text=${{ steps.health.outputs.message }}" \
      -d "parse_mode=HTML"
```

## 📊 Monitoring

### Check Workflow Status
1. Go to the **Actions** tab in your repository
2. Click on "Bot Health Check & Auto-Redeploy"
3. View recent runs and their status (green = success, red = failure)
4. Click on a run to see detailed logs

### Verify Bot Health
- You'll receive a ✅ HEALTHY message every 10 minutes in Telegram
- If you stop receiving messages, check the Actions tab for workflow errors
- Send a test command to your bot to manually verify it's responding

### Monitor Render Deployments
1. Open Render Dashboard
2. Go to your service
3. Check the **Events** or **Logs** tab
4. Look for "Deploy hook" triggered deployments

## 📈 Usage & Limits

### GitHub Actions Minutes

**Public Repositories:**
- ✅ Unlimited minutes - completely free!

**Private Repositories:**
- Free tier: 2,000 minutes per month
- Current usage: ~2,160 minutes/month (144 checks × 0.5 min each)
- ⚠️ Slightly exceeds free tier

**Solutions if you hit the limit:**
1. Make repository public (recommended)
2. Reduce frequency to every 15 or 20 minutes
3. Upgrade to GitHub Pro ($4/month for 3,000 minutes)
4. Only check during specific hours (e.g., 8 AM - 10 PM)

### Render Free Tier Limits
- Your bot may sleep after 15 minutes of inactivity
- This workflow will detect when it's down and automatically redeploy
- Each redeploy takes 2-3 minutes to complete

## 🐛 Troubleshooting

### Workflow Not Running Automatically
- **Check if scheduled**: GitHub Actions cron may have 3-15 minute delays
- **Verify default branch**: Workflows only run on default branch (usually `main`)
- **Check if disabled**: GitHub disables workflows after 60 days of repo inactivity
- **Manual test**: Use "Run workflow" button to verify it works

### Not Receiving Telegram Messages
- **Wrong BOT_TOKEN**: Verify token is correct in secrets
- **Wrong CHAT_ID**: Should be a number, get from [@userinfobot](https://t.me/userinfobot)
- **Bot blocked**: Make sure you haven't blocked the bot
- **Check workflow logs**: Go to Actions tab → Select a run → View logs

### Frequent Redeployments
- Your bot may be crashing repeatedly
- Check Render logs for errors in your bot code
- Verify database connections, API keys, and environment variables
- Consider increasing check interval to reduce noise

### Redeploy Not Triggering
- **Wrong REDEPLOY URL**: Verify the Render deploy hook URL is correct
- **Service suspended**: Check if your Render service is active
- **Check workflow logs**: Actions tab will show HTTP response codes
- **Manual test**: Copy the REDEPLOY URL and POST to it using curl or browser

### Bot Appears Down but It's Working
- Bot might be slow to respond (increase the 30-second wait)
- Temporary network issues between GitHub and Telegram
- Check workflow logs to see actual HTTP response codes

## 🔒 Security Best Practices

- Never commit secrets directly in workflow files
- Always use GitHub Secrets for sensitive data
- Regularly rotate your BOT_TOKEN and REDEPLOY hook
- Use a dedicated monitoring chat/group for CHAT_ID
- Review workflow run logs regularly for suspicious activity

## 📝 Notes

- GitHub Actions cron jobs may have a 3-15 minute delay during high traffic
- The workflow runs on GitHub servers, completely independent of your bot
- Even if Render shuts down your free instance, the workflow will detect and redeploy it
- First health check after bot startup might fail (bot needs 10-30 seconds to initialize)
- Workflow continues running even if your computer is off
- Each successful health check counts toward GitHub Actions minutes (if private repo)