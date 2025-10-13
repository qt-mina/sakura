# Workflow Automations

This directory contains GitHub Actions workflows for automating Sakura bot operations.

## 📋 Available Workflows

### `redeploy.yml` - Auto Redeploy Every 6 Hours

Automatically triggers a full redeploy of the bot on Render every 6 hours.

**Purpose:**
- Prevents memory leaks
- Ensures fresh bot instance
- Maintains optimal performance
- Clears cached data

**Schedule:**
- Runs every 6 hours (4 times daily)
- UTC times: 00:00, 06:00, 12:00, 18:00
- Bangladesh (GMT+6): 6 AM, 12 PM, 6 PM, 12 AM

**Manual Trigger:**
You can manually trigger this workflow:
1. Go to Actions tab
2. Select "Auto Redeploy Every 6 Hours"
3. Click "Run workflow"
4. Click the green "Run workflow" button

## 🔧 Configuration

### Required Secrets

- **REDEPLOY**: Render deploy hook URL
  - Get from: Render Dashboard → Service → Settings → Deploy Hook
  - Format: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`

### Modifying Schedule

To change the deployment frequency, edit the `cron` value in `redeploy.yml`:

```yaml
# Every 6 hours (current)
cron: '0 */6 * * *'

# Every 12 hours
cron: '0 */12 * * *'

# Every 3 hours
cron: '0 */3 * * *'

# Once daily at 6 AM Bangladesh time
cron: '0 0 * * *'

# Custom times (e.g., 6 AM and 6 PM only)
cron: '0 0,12 * * *'
```

## 📊 Monitoring

### Check Workflow Status
1. Go to the **Actions** tab in your repository
2. Click on "Auto Redeploy Every 6 Hours"
3. View recent runs and their status

### Verify Render Deployments
1. Open Render Dashboard
2. Go to your service
3. Check the **Events** or **Logs** tab
4. Look for "Deploy hook" triggered deployments

## 🐛 Troubleshooting

### Workflow Not Running
- Check if Actions are enabled in repository settings
- Verify the cron syntax is correct
- Ensure the workflow file is in the correct path

### Deployment Failing
- Verify the `REDEPLOY` secret contains the correct URL
- Check Render service status
- Review workflow logs in Actions tab

### Wrong Timing
- Remember: cron uses UTC time
- Convert your local time to UTC
- Bangladesh (GMT+6) = UTC + 6 hours

## 📝 Notes

- GitHub Actions cron jobs may have a 3-15 minute delay during high traffic
- The workflow runs on GitHub servers, independent of your bot's status
- Even if Render shuts down your free instance, the workflow will wake it up and redeploy