"""
Example: Custom OPEX alert script

This example shows how to customize the OPEX alerts for specific use cases.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from opex_alerts import OPEXCalculator, DiscordWebhook, get_next_opex


def send_weekly_opex_reminder():
    """Send OPEX reminders for dates within the next 7 days."""
    load_dotenv()
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set")
        return
    
    discord = DiscordWebhook(webhook_url)
    opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
    
    today = datetime.now()
    week_from_now = today + timedelta(days=7)
    
    # Find OPEX dates within the next week
    upcoming_opex = [d for d in opex_dates 
                     if today.date() <= d.date() <= week_from_now.date()]
    
    if upcoming_opex:
        for opex_date in upcoming_opex:
            days_until = (opex_date.date() - today.date()).days
            discord.send_opex_alert(opex_date, days_until)
            print(f"✓ Sent reminder for {opex_date.strftime('%B %d, %Y')} ({days_until} days)")
    else:
        print("No OPEX dates in the next 7 days")


def send_monthly_calendar():
    """Send the full OPEX calendar at the start of each month."""
    load_dotenv()
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set")
        return
    
    discord = DiscordWebhook(webhook_url)
    opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
    
    if discord.send_opex_calendar(2026, opex_dates):
        print("✓ Monthly OPEX calendar sent")
    else:
        print("✗ Failed to send calendar")


def send_custom_alert():
    """Send a custom formatted alert."""
    load_dotenv()
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL not set")
        return
    
    discord = DiscordWebhook(webhook_url)
    opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
    next_opex = get_next_opex(opex_dates)
    
    if next_opex:
        # Custom message with trading tips
        custom_message = f"""
        🚨 **OPEX Alert** 🚨
        
        Next options expiration: **{next_opex.strftime('%B %d, %Y')}**
        
        📌 Reminder:
        • Review your options positions
        • Consider rolling or closing positions
        • Plan for potential volatility
        • Check your risk management strategy
        """
        
        discord.send_message(custom_message.strip())
        print("✓ Custom alert sent")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_custom_alerts.py [weekly|monthly|custom]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "weekly":
        send_weekly_opex_reminder()
    elif mode == "monthly":
        send_monthly_calendar()
    elif mode == "custom":
        send_custom_alert()
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: weekly, monthly, custom")
        sys.exit(1)
