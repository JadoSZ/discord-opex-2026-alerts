# Discord OPEX 2026 Alerts Bot

An automated Discord bot that sends timely alerts for Options Expiration (OPEX) events. The bot reads OPEX dates from a PDF calendar and sends scheduled alerts to your Discord channel.

## Features

- **D-1 Alerts**: Automatically sends alerts one day before OPEX at 16:00 PM Eastern Time
- **D-0 Alerts**: Automatically sends alerts on OPEX day at 09:00 AM Eastern Time
- **Weekly Previews**: Every Sunday at 18:00 PM Eastern, sends a preview of upcoming OPEX events for the week (only if events exist)
- **PDF Calendar Parsing**: Extracts OPEX dates from PDF calendar files
- **Discord Commands**: Interactive commands to check next OPEX date and list all dates

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Discord bot token (see below)
- A Discord server where you have admin permissions

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT (optional)
5. Copy the bot token (you'll need this later)
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot`
8. Select bot permissions: `Send Messages`, `Embed Links`, `Read Message History`
9. Copy the generated URL and open it in your browser to invite the bot to your server

### 3. Get Your Channel ID

1. In Discord, go to User Settings > Advanced
2. Enable "Developer Mode"
3. Right-click on your desired alert channel
4. Click "Copy ID"

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your values:
```
DISCORD_TOKEN=your_actual_bot_token_here
CHANNEL_ID=your_actual_channel_id_here
CALENDAR_PDF_PATH=opex_calendar.pdf
```

### 6. Prepare Your OPEX Calendar

You have two options:

#### Option A: Use the Sample Calendar
Generate a sample 2026 OPEX calendar:
```bash
python create_sample_calendar.py
```

This creates `opex_calendar.pdf` with standard monthly OPEX dates (third Friday of each month).

#### Option B: Use Your Own PDF Calendar
Place your OPEX calendar PDF file in the project directory and update the `CALENDAR_PDF_PATH` in `.env`

The PDF should contain dates in one of these formats:
- MM/DD/YYYY (e.g., 01/16/2026)
- Month DD, YYYY (e.g., January 16, 2026)

### 7. Run the Bot

```bash
python bot.py
```

The bot will:
- Connect to Discord
- Parse the OPEX calendar
- Start scheduled alert tasks
- Begin monitoring for alert times

## Alert Schedule

| Alert Type | Time (Eastern) | Description |
|------------|----------------|-------------|
| D-1 Alert | 16:00 PM (4:00 PM) | One day before OPEX |
| D-0 Alert | 09:00 AM (9:00 AM) | Morning of OPEX day |
| Weekly Preview | Sunday 18:00 PM (6:00 PM) | Preview of upcoming week's events |

## Bot Commands

Use these commands in your Discord server:

- `!nextopex` - Shows the next upcoming OPEX date
- `!listopex` - Lists all OPEX dates from the calendar
- `!reload` - (Admin only) Reloads the calendar from the PDF file

## Project Structure

```
discord-opex-2026-alerts/
├── bot.py                      # Main bot application
├── calendar_parser.py          # PDF calendar parsing logic
├── create_sample_calendar.py   # Script to generate sample calendar
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Deployment

### Running 24/7

For production use, consider these options:

#### Option 1: Cloud Hosting
- Deploy to services like Heroku, Railway, or Google Cloud Run
- Ensure the service stays running 24/7

#### Option 2: VPS/Server
- Run on a VPS (DigitalOcean, Linode, AWS EC2)
- Use a process manager like `systemd` or `pm2`

#### Option 3: Container
- Use Docker to containerize the bot
- Deploy to Kubernetes or Docker Swarm

### Using systemd (Linux)

Create a service file at `/etc/systemd/system/opex-bot.service`:

```ini
[Unit]
Description=Discord OPEX Alerts Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/discord-opex-2026-alerts
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable opex-bot
sudo systemctl start opex-bot
```

## Troubleshooting

### Bot doesn't connect
- Verify your `DISCORD_TOKEN` is correct
- Ensure the bot is invited to your server with proper permissions

### No alerts being sent
- Check that `CHANNEL_ID` is correct
- Verify the bot has permissions to send messages in the channel
- Check the calendar was parsed successfully (look at logs)

### Calendar not parsing correctly
- Ensure your PDF contains dates in supported formats
- Check the logs for parsing errors
- Try the sample calendar first to verify setup

## Customization

### Changing Alert Times
Edit the time checks in `bot.py`:
- D-1 alerts: Modify line with `if now.hour == 16 and now.minute == 0:`
- D-0 alerts: Modify line with `if now.hour == 9 and now.minute == 0:`
- Weekly preview: Modify line with `if now.weekday() == 6 and now.hour == 18 and now.minute == 0:`

### Changing Alert Messages
Customize the embed messages in the respective functions:
- `d_minus_1_alert()`
- `d_0_alert()`
- `weekly_preview()`

## License

MIT License - feel free to modify and use as needed.

## Support

For issues or questions, please open an issue on GitHub.