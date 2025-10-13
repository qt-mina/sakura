# GitHub Automation

This directory contains GitHub-specific configurations and automations for the Sakura bot.

## 📁 Structure

- `workflows/` - GitHub Actions workflow files for automated tasks

## 🔧 Workflows

### Auto Redeploy Every 6 Hours
Automatically triggers a Render redeploy every 6 hours to keep the bot fresh and prevent memory leaks.

**Schedule (Bangladesh Time GMT+6):**
- 6:00 AM
- 12:00 PM
- 6:00 PM
- 12:00 AM

## 🔐 Secrets Required

The following secrets must be configured in GitHub repository settings:

- `REDEPLOY` - Render deploy hook URL for triggering redeployments

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Deploy Hooks](https://render.com/docs/deploy-hooks)
