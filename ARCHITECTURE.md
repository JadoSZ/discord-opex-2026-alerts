# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Discord OPEX Alerts Bot                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────┐
        │            bot.py (Main Bot)             │
        │  ┌────────────────────────────────────┐  │
        │  │  Discord.py Client & Commands      │  │
        │  │  - !nextopex, !listopex, !reload   │  │
        │  └────────────────────────────────────┘  │
        │  ┌────────────────────────────────────┐  │
        │  │     Scheduled Alert Tasks          │  │
        │  │  - d_minus_1_alert (16:00 PM ET)   │  │
        │  │  - d_0_alert (09:00 AM ET)         │  │
        │  │  - weekly_preview (Sun 18:00 PM)   │  │
        │  └────────────────────────────────────┘  │
        └──────────────┬───────────────────────────┘
                       │
                       │ Uses
                       ▼
        ┌──────────────────────────────────────────┐
        │      calendar_parser.py                  │
        │  ┌────────────────────────────────────┐  │
        │  │   PDF Parsing (PyPDF2)             │  │
        │  │   - Extract text from PDF          │  │
        │  │   - Parse dates with regex         │  │
        │  └────────────────────────────────────┘  │
        │  ┌────────────────────────────────────┐  │
        │  │   Date Management                  │  │
        │  │   - get_next_opex_date()           │  │
        │  │   - get_opex_dates_in_week()       │  │
        │  └────────────────────────────────────┘  │
        └──────────────┬───────────────────────────┘
                       │
                       │ Reads
                       ▼
        ┌──────────────────────────────────────────┐
        │      opex_calendar.pdf                   │
        │  (User-provided or generated)            │
        └──────────────────────────────────────────┘
```

## Data Flow

```
1. Bot Startup
   ├─► Load environment variables (.env)
   ├─► Initialize Discord client
   ├─► Parse PDF calendar
   └─► Start scheduled tasks

2. Alert Scheduling
   ├─► Every minute, check current time (Eastern)
   ├─► If time matches alert schedule:
   │   ├─► Query calendar for relevant OPEX dates
   │   ├─► Format Discord embed message
   │   └─► Send to configured channel
   └─► Log alert activity

3. User Commands
   ├─► !nextopex
   │   └─► Query next upcoming OPEX date
   ├─► !listopex
   │   └─► Display all OPEX dates by month
   └─► !reload
       └─► Re-parse PDF calendar
```

## Alert Types

### D-1 Alert (Orange)
- **Trigger**: Day before OPEX at 16:00 PM ET
- **Purpose**: Give advance notice
- **Content**: Date, time remaining

### D-0 Alert (Red)
- **Trigger**: OPEX day at 09:00 AM ET
- **Purpose**: Day-of reminder at market open
- **Content**: Date, market status

### Weekly Preview (Blue)
- **Trigger**: Sunday at 18:00 PM ET
- **Condition**: Only if events exist in upcoming week
- **Content**: All OPEX dates for the week, days until each

## Configuration

```
Environment Variables (.env)
├─► DISCORD_TOKEN: Bot authentication
├─► CHANNEL_ID: Target alert channel
└─► CALENDAR_PDF_PATH: Path to calendar file

Dependencies (requirements.txt)
├─► discord.py: Discord API client
├─► python-dotenv: Environment management
├─► pytz: Timezone handling
├─► PyPDF2: PDF parsing
└─► reportlab: PDF generation (sample calendar)
```

## Deployment Options

```
┌─────────────┬──────────────────────────────────────┐
│ Local       │ python bot.py                        │
├─────────────┼──────────────────────────────────────┤
│ Docker      │ docker-compose up -d                 │
├─────────────┼──────────────────────────────────────┤
│ VPS/Server  │ systemd service (24/7 operation)     │
├─────────────┼──────────────────────────────────────┤
│ Cloud       │ Heroku, Railway, GCP, etc.           │
└─────────────┴──────────────────────────────────────┘
```
