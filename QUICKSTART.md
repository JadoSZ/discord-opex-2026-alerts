# Quick Start Guide

## 1. Get Discord Bot Token
1. Visit https://discord.com/developers/applications
2. Create new application → Bot → Add Bot
3. Enable MESSAGE CONTENT INTENT
4. Copy the bot token

## 2. Invite Bot to Your Server
1. Go to OAuth2 → URL Generator
2. Select: `bot` scope
3. Select permissions: Send Messages, Embed Links, Read Message History
4. Use generated URL to invite bot

## 3. Get Channel ID
1. Discord Settings → Advanced → Enable Developer Mode
2. Right-click your alerts channel → Copy ID

## 4. Setup & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your values:
# - DISCORD_TOKEN=your_bot_token
# - CHANNEL_ID=your_channel_id

# Generate sample calendar (or use your own PDF)
python create_sample_calendar.py

# Run the bot
python bot.py
```

## 5. Test Commands
In Discord, try:
- `!nextopex` - See next OPEX date
- `!listopex` - List all OPEX dates
- `!reload` - (Admin) Reload calendar

## Alert Schedule
- **D-1**: 16:00 PM ET (day before OPEX)
- **D-0**: 09:00 AM ET (OPEX day)
- **Weekly**: Sunday 18:00 PM ET (preview)

## Docker Deployment (Optional)
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## Troubleshooting
- **Bot won't connect**: Check DISCORD_TOKEN
- **No alerts**: Verify CHANNEL_ID and bot permissions
- **Calendar issues**: Check PDF format, try sample calendar first
