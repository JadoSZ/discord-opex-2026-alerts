# Example Configuration for Discord OPEX Alerts

## Environment Setup

Create a `.env` file with your Discord webhook URL:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

## Alert Frequency Levels

### Low Frequency (16 events)
Best for: Traders who only want major monthly and quarterly events

```bash
python opex_alerts.py --alert-type d1 --frequency low
```

Includes:
- 12 Standard monthly expirations
- 4 Quarterly (end-of-quarter) expirations

### Medium Frequency (41 events) - RECOMMENDED
Best for: Most users - covers all major market events

```bash
python opex_alerts.py --alert-type d1 --frequency medium
```

Includes:
- 12 Standard monthly expirations
- 12 VIX options expirations
- 4 Quarterly (end-of-quarter) expirations
- 3 LEAPS additions
- 10 Exchange holidays

### High Frequency (53 events)
Best for: Active options traders who need all event notifications

```bash
python opex_alerts.py --alert-type d1 --frequency high
```

Includes:
- 12 Standard monthly expirations
- 12 VIX options expirations
- 12 AM-settled last trading days
- 4 Quarterly (end-of-quarter) expirations
- 3 LEAPS additions
- 10 Exchange holidays

## Alert Timing Examples

### Multi-Day Alerts (1-3 days before events)

```bash
# 3 days before events
python opex_alerts.py --alert-type d3 --frequency medium

# 2 days before events
python opex_alerts.py --alert-type d2 --frequency medium

# 1 day before events (at 4:00 PM ET)
python opex_alerts.py --alert-type d1 --frequency medium

# Day of event (at 9:30 AM ET)
python opex_alerts.py --alert-type d0 --frequency medium
```

### Weekly Preview

Get a Sunday evening overview of the upcoming week:

```bash
python opex_alerts.py --alert-type weekly --frequency medium
```

### Test All Alert Formats

Preview all alert types without waiting for scheduled times:

```bash
python opex_alerts.py --alert-type test --frequency medium
```

## GitHub Actions Schedule

The automated workflows run at these times (all Eastern Time):

| Alert Type | Time | Frequency | Description |
|------------|------|-----------|-------------|
| D-3 | 4:00 PM ET daily | Checks 3 days ahead | Early warning |
| D-2 | 4:00 PM ET daily | Checks 2 days ahead | Mid-range notice |
| D-1 | 4:00 PM ET daily | Checks 1 day ahead | Next day reminder |
| D-0 | 9:30 AM ET daily | Checks today | Day-of alert at market open |
| Weekly | 6:00 PM ET Sunday | Next 7 days | Week preview |

## Custom Calendar File

To use a custom calendar JSON file:

```bash
python opex_alerts.py --alert-type d1 --frequency medium --calendar-file /path/to/custom_calendar.json
```

## Docker Usage

Run with Docker Compose:

```bash
# Set environment variables in docker-compose.yml
DISCORD_WEBHOOK_URL=your_webhook_url

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

## Testing Without Sending Alerts

To validate the calendar data and logic without sending Discord messages:

```bash
# Run unit tests
python -m unittest test_opex_alerts -v

# Dry run (will fail if webhook not set, but shows logic)
python opex_alerts.py --alert-type d1 --frequency medium
```

## Event Type Customization

If you want alerts for specific event types only, you can:

1. Create a custom calendar JSON with only desired event types
2. Modify the `alert_frequencies` section in `calendar_2026.json`
3. Use the appropriate frequency level (low/medium/high)

Example custom frequency in `calendar_2026.json`:

```json
"custom": {
  "description": "VIX and Standard only",
  "includes": [
    "standard_expirations",
    "vix_standard_expirations"
  ]
}
```

Then modify `opex_alerts.py` to support the "custom" frequency option.

## Important Dates to Note

### 2026 Irregular Dates
- **June 18 (Thursday)**: Standard expiration moved due to Juneteenth on Friday June 19
- **June 17 (Wednesday)**: AM-settled last trading day (instead of Thursday)

### Exchange Holidays (Market Closed)
- January 1 (Thursday) - New Year's Day
- January 19 (Monday) - MLK Jr. Day
- February 16 (Monday) - Presidents' Day
- April 3 (Friday) - Good Friday
- May 25 (Monday) - Memorial Day
- June 19 (Friday) - Juneteenth
- July 3 (Friday) - Independence Day observed
- September 7 (Monday) - Labor Day
- November 26 (Thursday) - Thanksgiving
- December 25 (Friday) - Christmas

## Troubleshooting

### Webhook Not Working
- Verify your webhook URL is correct in `.env`
- Check that the webhook hasn't been deleted in Discord
- Ensure your server has proper permissions

### No Alerts Sent
- Check that today/tomorrow actually has an event
- Verify the frequency level includes the event type
- Run with `--alert-type test` to see all event types

### Calendar Not Loading
- Ensure `calendar_2026.json` exists in the same directory
- Validate JSON syntax with `python -m json.tool calendar_2026.json`
- Check file permissions

## Support

For issues or questions:
- Check the README.md
- Review test files for examples
- Open an issue on GitHub
