# Discord OPEX 2026 Alerts

A Python script that sends Discord notifications for Options Expiration (OPEX) dates in 2026. OPEX occurs on the third Friday of each month, and this tool helps traders and investors stay informed about upcoming expiration dates.

## Features

- 📅 Calculates all OPEX dates for 2026 (third Friday of each month)
- 🔔 Sends Discord alerts for upcoming OPEX dates
- 📊 Displays a full OPEX calendar for the year
- ⏰ Shows days remaining until next OPEX
- 🎨 Rich embed formatting with color-coded alerts
- 🤖 **Automated alerts via GitHub Actions**
  - Weekly preview (Sundays at 18:00 ET)
  - D-1 alerts (day before at 16:00 ET)
  - D-0 alerts (day of at 09:30 ET)

## 🧪 Quick Test

To verify your Discord webhook is working:

1. Go to [Actions](https://github.com/JadoSZ/discord-opex-2026-alerts/actions)
2. Click **"Test Discord Webhook"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Check your Discord channel - you should see a **green test message** immediately!

This test works regardless of the current date and will always send a message.

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/JadoSZ/discord-opex-2026-alerts.git
cd discord-opex-2026-alerts
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Discord webhook:
   - Go to your Discord server settings
   - Navigate to Integrations → Webhooks
   - Create a new webhook or copy an existing webhook URL
   - Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your webhook URL:
   ```
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_id/your_webhook_token
   ```

## Usage

### Manual Execution

Run the script to send OPEX alerts to your Discord channel:

```bash
# Send full calendar (default)
python opex_alerts.py

# Send weekly preview (only if OPEX in next 7 days)
python opex_alerts.py --alert-type weekly

# Send D-1 alert (only if tomorrow is OPEX)
python opex_alerts.py --alert-type d1

# Send D-0 alert (only if today is OPEX)
python opex_alerts.py --alert-type d0
```

### Test Webhook

Test your Discord webhook connection:

```bash
# Using environment variable from .env
python test_webhook.py

# Using command line argument
python test_webhook.py https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
```

This will:
1. Send a complete OPEX calendar for 2026 showing all 12 expiration dates
2. Send an alert for the next upcoming OPEX date with days remaining

## Alert Types

The system supports different alert types with distinct messaging and colors:

### Weekly Preview (Blue - Informational)
```
📅 OPEX Week Preview
Next OPEX: January 16, 2026
⏰ 5 days remaining
Get ready for next Friday's expiration!
```

### D-1 Alert (Orange - Warning)
```
⚠️ OPEX TOMORROW!
Date: January 16, 2026
Time to review your positions
Market closes in ~24 hours until expiration
```

### D-0 Alert (Red - Urgent)
```
🚨 TODAY IS OPEX!
Date: January 16, 2026
Market is NOW OPEN
Options expire at market close (4:00 PM ET)
```

## OPEX Dates for 2026

The script automatically calculates the third Friday of each month:

- January 16, 2026
- February 20, 2026
- March 20, 2026
- April 17, 2026
- May 15, 2026
- June 19, 2026
- July 17, 2026
- August 21, 2026
- September 18, 2026
- October 16, 2026
- November 20, 2026
- December 18, 2026

## Automation

### GitHub Actions (Recommended)

This repository includes automated workflows that run on schedule:

#### 1. Weekly Preview Alert
- **Schedule**: Every Sunday at 18:00 PM Eastern (22:00 UTC)
- **Behavior**: Only sends if there's an OPEX date in the next 7 days
- **Message**: Blue informational alert with days remaining
- **Workflow**: `.github/workflows/weekly-preview.yml`

#### 2. D-1 Alert (Day Before)
- **Schedule**: Daily at 16:00 PM Eastern (20:00 UTC)
- **Behavior**: Only sends if tomorrow is an OPEX date
- **Message**: Orange warning alert with preparation reminder
- **Workflow**: `.github/workflows/d1-alert.yml`

#### 3. D-0 Alert (Day Of)
- **Schedule**: Daily at 09:30 AM Eastern (13:30 UTC)
- **Behavior**: Only sends if today is an OPEX date
- **Message**: Red urgent alert with market open notification
- **Workflow**: `.github/workflows/d0-alert.yml`

#### Setup GitHub Actions

1. Fork this repository to your own GitHub account
2. Go to your repository Settings → Secrets and variables → Actions
3. Add a new repository secret:
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Your Discord webhook URL
4. The workflows will run automatically on schedule
5. You can also trigger them manually from the Actions tab

**Note**: The workflows only send alerts when conditions are met (e.g., OPEX is coming up), so they won't spam your channel.

## Testing the Alerts

You can test the alerts manually without waiting for scheduled times:

### Test Individual Alerts

1. Go to [Actions](https://github.com/JadoSZ/discord-opex-2026-alerts/actions)
2. Select the workflow you want to test:
   - **Weekly Preview** - Sunday preview alert
   - **D-1 Alert** - Day before alert
   - **D-0 Alert** - Day of OPEX alert
3. Click "Run workflow" dropdown
4. Click "Run workflow" button
5. Check your Discord channel for the alert

### Test All Alerts at Once

1. Go to [Actions](https://github.com/JadoSZ/discord-opex-2026-alerts/actions)
2. Select "Test All Alerts" workflow
3. Click "Run workflow" dropdown
4. Click "Run workflow" button
5. All three alert types will be sent in sequence (10 seconds total)

**Note:** The test workflow uses current dates, so alerts may say "No upcoming OPEX" depending on when you run it.

### Manual Scheduling

You can also automate this script to run on a schedule using:

#### Cron (Linux/Mac)
```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/discord-opex-2026-alerts && python opex_alerts.py
```

#### Task Scheduler (Windows)
Create a scheduled task to run `python opex_alerts.py` at your desired frequency.

## Requirements

- Python 3.7+
- `requests` library for HTTP requests
- `python-dotenv` for environment variable management

## Contributing

Feel free to open issues or submit pull requests for improvements!

## License

MIT License - feel free to use this for your trading and investment activities.
