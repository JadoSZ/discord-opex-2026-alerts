# Discord OPEX 2026 Alerts

A Python script that sends Discord notifications for Options Expiration (OPEX) dates in 2026. OPEX occurs on the third Friday of each month, and this tool helps traders and investors stay informed about upcoming expiration dates.

## Features

- 📅 Calculates all OPEX dates for 2026 (third Friday of each month)
- 🔔 Sends Discord alerts for upcoming OPEX dates
- 📊 Displays a full OPEX calendar for the year
- ⏰ Shows days remaining until next OPEX
- 🎨 Rich embed formatting with color-coded alerts

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

Run the script to send OPEX alerts to your Discord channel:

```bash
python opex_alerts.py
```

This will:
1. Send a complete OPEX calendar for 2026 showing all 12 expiration dates
2. Send an alert for the next upcoming OPEX date with days remaining

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

You can automate this script to run on a schedule using:

### Cron (Linux/Mac)
```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/discord-opex-2026-alerts && python opex_alerts.py
```

### Task Scheduler (Windows)
Create a scheduled task to run `python opex_alerts.py` at your desired frequency.

### GitHub Actions
You can also set up GitHub Actions to run this on a schedule. See `.github/workflows/` directory for examples.

## Requirements

- Python 3.7+
- `requests` library for HTTP requests
- `python-dotenv` for environment variable management

## Contributing

Feel free to open issues or submit pull requests for improvements!

## License

MIT License - feel free to use this for your trading and investment activities.
