# Discord OPEX 2026 Alerts

Automated Discord alerts for Options Expiration (OPEX) dates in 2026 based on the official CBOE calendar.

## Features

### Comprehensive 2026 Calendar Coverage
- **Standard Options Expirations**: 12 monthly expirations (3rd Friday, adjusted for holidays)
- **VIX Options**: 12 monthly VIX standard expirations with last trading days
- **AM-Settled Index Options**: Last trading day alerts (day before expiration)
- **End-of-Month/Quarter Expirations**: Quarterly options expirations
- **LEAPS Additions**: 2029 LEAPS series introduction dates
- **Exchange Holidays**: 10 market holidays with proper notifications
- **Special Notes**: Irregular dates marked (e.g., June 18 Thursday due to Juneteenth)

### Multi-Day Alert System
Receive alerts **1-3 days in advance** of important dates:
- **D-3 Alert**: 3 days before event
- **D-2 Alert**: 2 days before event
- **D-1 Alert**: 1 day before event (day before at 4:00 PM ET)
- **D-0 Alert**: Day of event (market open at 9:30 AM ET)
- **Weekly Preview**: Sunday evening overview of upcoming week

### Alert Frequency Levels
Choose your preferred alert frequency:

| Level | Description | Events Included | Total Events |
|-------|-------------|-----------------|--------------|
| **Low** | Monthly + Quarterly only | Standard expirations + End-of-quarter | 16 events |
| **Medium** | Standard + VIX + Quarterly + LEAPS | All major events + holidays | 41 events |
| **High** | All events including weeklys | Complete calendar with all event types | 53+ events |

### Event-Specific Alert Formats
Each event type has a custom Discord embed with relevant information:
- 📅 **Standard Expirations**: Date, type, special notes
- 📊 **VIX Options**: Expiration date + last trading day
- ⏰ **AM-Settled Index**: Last trading day + next day expiration
- 📆 **End-of-Month/Quarter**: Quarterly expiration notifications
- 🆕 **LEAPS Additions**: New long-term series availability
- 🏦 **Exchange Holidays**: Market closure notifications

### Special 2026 Features
- **Irregular June Expiration**: June 18 (Thursday) instead of Friday due to Juneteenth
- **Holiday Proximity Warnings**: Alerts when expirations are near holidays
- **Weekend Adjustments**: Alerts automatically move to Friday if they would fall on weekends

## Installation

### Requirements
- Python 3.11+
- Discord webhook URL
- Required packages: `requests`, `python-dotenv`

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file:
```env
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

2. The calendar data is stored in `calendar_2026.json` (included in repository)

## Usage

### Command Line

```bash
# Send D-1 alert (1 day before events) - Medium frequency
python opex_alerts.py --alert-type d1 --frequency medium

# Send D-2 alert (2 days before events)
python opex_alerts.py --alert-type d2 --frequency medium

# Send D-3 alert (3 days before events)
python opex_alerts.py --alert-type d3 --frequency medium

# Send D-0 alert (day of events)
python opex_alerts.py --alert-type d0 --frequency medium

# Send weekly preview
python opex_alerts.py --alert-type weekly --frequency medium

# Test all alert formats
python opex_alerts.py --alert-type test --frequency medium

# Send full calendar (backward compatibility)
python opex_alerts.py --alert-type calendar
```

### Frequency Options

```bash
# Low frequency: Only monthly standard + quarterly (16 events)
python opex_alerts.py --alert-type d1 --frequency low

# Medium frequency: Standard + VIX + quarterly + LEAPS (41 events)
python opex_alerts.py --alert-type d1 --frequency medium

# High frequency: All events (53+ events)
python opex_alerts.py --alert-type d1 --frequency high
```

## GitHub Actions Automation

Automated workflows run daily to send alerts:

- **D-3 Alert**: Daily at 4:00 PM ET (checks 3 days ahead)
- **D-2 Alert**: Daily at 4:00 PM ET (checks 2 days ahead)  
- **D-1 Alert**: Daily at 4:00 PM ET (checks 1 day ahead)
- **D-0 Alert**: Daily at 9:30 AM ET (day-of notification)
- **Weekly Preview**: Every Sunday at 6:00 PM ET

All workflows can be manually triggered via GitHub Actions interface for testing.

## Calendar Data

The `calendar_2026.json` file contains all 2026 CBOE calendar data:
- Exchange holidays with names
- Standard monthly expirations (including irregular June 18)
- VIX options with last trading days
- AM-settled index last trading days
- End-of-month/quarter expirations
- 2029 LEAPS addition dates

### Example Event Structure

```json
{
  "date": "2026-06-18",
  "day_of_week": "Thursday",
  "type": "Equity, Equity Index, ETF & ETN Options",
  "notes": "⚠️ Note: Expiration moved to Thursday due to Juneteenth holiday on Friday"
}
```

## Testing

Run the test suite:

```bash
python -m unittest test_opex_alerts -v
```

Test all alert formats:

```bash
python opex_alerts.py --alert-type test --frequency medium
```

## 2026 Key Dates

### Irregular Dates
- **June 18, 2026 (Thursday)**: Standard expiration moved due to Juneteenth on June 19

### Holiday Impact
- July 3 (Friday) - Independence Day observed (note added to July 17 expiration)

### Quarterly Expirations
- March 31 (Tuesday) - Q1 End
- June 30 (Tuesday) - Q2 End  
- September 30 (Wednesday) - Q3 End
- December 31 (Thursday) - Q4 End

## Docker Support

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Contributing

Contributions are welcome! Please ensure:
- All tests pass before submitting PRs
- Calendar data follows CBOE official dates
- Alert formats are consistent with existing patterns

## License

MIT License - See LICENSE file for details