"""
Discord OPEX 2026 Alerts

This module provides OPEX (Options Expiration) dates for 2026 and sends alerts to Discord.
Uses official CBOE 2026 calendar with holiday adjustments.
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv


class OPEXCalculator:
    """Calculate OPEX dates for a given year with CBOE holiday adjustments."""
    
    # CBOE 2026 Monthly Options Expiration dates (with holiday adjustments)
    # June 18 is Thursday due to Juneteenth holiday on June 19
    CBOE_2026_DATES = [
        datetime(2026, 1, 16),   # January 16 (Friday)
        datetime(2026, 2, 20),   # February 20 (Friday)
        datetime(2026, 3, 20),   # March 20 (Friday)
        datetime(2026, 4, 17),   # April 17 (Friday)
        datetime(2026, 5, 15),   # May 15 (Friday)
        datetime(2026, 6, 18),   # June 18 (Thursday - Juneteenth adjustment)
        datetime(2026, 7, 17),   # July 17 (Friday)
        datetime(2026, 8, 21),   # August 21 (Friday)
        datetime(2026, 9, 18),   # September 18 (Friday)
        datetime(2026, 10, 16),  # October 16 (Friday)
        datetime(2026, 11, 20),  # November 20 (Friday)
        datetime(2026, 12, 18),  # December 18 (Friday)
    ]
    
    @staticmethod
    def get_third_friday(year: int, month: int) -> datetime:
        """
        Calculate the third Friday of a given month and year.
        
        Args:
            year: The year
            month: The month (1-12)
            
        Returns:
            datetime object for the third Friday
        """
        # Start with the first day of the month
        first_day = datetime(year, month, 1)
        
        # Find the first Friday (weekday 4 = Friday)
        days_until_friday = (4 - first_day.weekday()) % 7
        first_friday = first_day + timedelta(days=days_until_friday)
        
        # Add two more weeks to get the third Friday
        third_friday = first_friday + timedelta(weeks=2)
        
        return third_friday
    
    @staticmethod
    def get_opex_dates_for_year(year: int) -> List[datetime]:
        """
        Get all OPEX dates for a given year.
        For 2026, returns official CBOE dates with holiday adjustments.
        For other years, calculates third Friday of each month.
        
        Args:
            year: The year to calculate OPEX dates for
            
        Returns:
            List of datetime objects for each OPEX date
        """
        if year == 2026:
            # Return official CBOE 2026 dates with holiday adjustments
            return OPEXCalculator.CBOE_2026_DATES.copy()
        else:
            # For other years, calculate third Friday
            opex_dates = []
            for month in range(1, 13):
                opex_date = OPEXCalculator.get_third_friday(year, month)
                opex_dates.append(opex_date)
            return opex_dates


class DiscordWebhook:
    """Handle Discord webhook notifications."""
    
    def __init__(self, webhook_url: str):
        """
        Initialize the Discord webhook.
        
        Args:
            webhook_url: The Discord webhook URL
        """
        self.webhook_url = webhook_url
    
    def send_message(self, content: str, embeds: Optional[List[Dict]] = None) -> bool:
        """
        Send a message to Discord via webhook.
        
        Args:
            content: The message content
            embeds: Optional list of embed objects
            
        Returns:
            True if successful, False otherwise
        """
        payload = {"content": content}
        
        if embeds:
            payload["embeds"] = embeds
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to Discord: {e}")
            return False
    
    def send_opex_alert(self, opex_date: datetime, days_until: int) -> bool:
        """
        Send an OPEX alert to Discord.
        
        Args:
            opex_date: The OPEX date
            days_until: Days until OPEX
            
        Returns:
            True if successful, False otherwise
        """
        embed = {
            "title": "📅 OPEX Alert",
            "description": f"Options Expiration Date: **{opex_date.strftime('%B %d, %Y')}**",
            "color": 0xFF5733,  # Orange color
            "fields": [
                {
                    "name": "Days Until OPEX",
                    "value": str(days_until),
                    "inline": True
                },
                {
                    "name": "Day of Week",
                    "value": opex_date.strftime('%A'),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"🔔 OPEX Alert: {days_until} days until options expiration!"
        return self.send_message(content, embeds=[embed])
    
    def send_opex_calendar(self, year: int, opex_dates: List[datetime]) -> bool:
        """
        Send a full OPEX calendar to Discord.
        
        Args:
            year: The year
            opex_dates: List of OPEX dates
            
        Returns:
            True if successful, False otherwise
        """
        # Create fields for each month
        fields = []
        for opex_date in opex_dates:
            fields.append({
                "name": opex_date.strftime('%B'),
                "value": opex_date.strftime('%B %d, %Y (%A)'),
                "inline": True
            })
        
        # Update description to note holiday adjustments
        description = f"All options expiration dates for {year}"
        if year == 2026:
            description += " (CBOE official calendar with holiday adjustments)"
        else:
            description += " (Third Friday of each month)"
        
        embed = {
            "title": f"📊 OPEX Calendar {year}",
            "description": description,
            "color": 0x3498DB,  # Blue color
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📆 OPEX Calendar for {year}"
        return self.send_message(content, embeds=[embed])
    
    def send_weekly_preview(self, opex_date: datetime, days_until: int) -> bool:
        """
        Send a weekly preview alert for upcoming OPEX.
        
        Args:
            opex_date: The OPEX date
            days_until: Days until OPEX
            
        Returns:
            True if successful, False otherwise
        """
        # Adjust reminder text based on day of week
        day_name = opex_date.strftime('%A')
        if day_name == 'Friday':
            reminder = "Get ready for next Friday's expiration!"
        elif day_name == 'Thursday':
            reminder = "Get ready for Thursday's expiration (holiday adjusted)!"
        else:
            reminder = f"Get ready for {day_name}'s expiration!"
        
        embed = {
            "title": "📅 OPEX Week Preview",
            "description": f"Next OPEX: **{opex_date.strftime('%B %d, %Y')}**",
            "color": 0x3498DB,  # Blue - Informational
            "fields": [
                {
                    "name": "⏰ Days Remaining",
                    "value": str(days_until),
                    "inline": True
                },
                {
                    "name": "Day of Week",
                    "value": opex_date.strftime('%A'),
                    "inline": True
                },
                {
                    "name": "📋 Reminder",
                    "value": reminder,
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📅 **OPEX Week Preview** - {days_until} days until options expiration"
        return self.send_message(content, embeds=[embed])
    
    def send_d1_alert(self, opex_date: datetime) -> bool:
        """
        Send a D-1 (day before) alert for OPEX.
        
        Args:
            opex_date: The OPEX date (tomorrow)
            
        Returns:
            True if successful, False otherwise
        """
        embed = {
            "title": "⚠️ OPEX TOMORROW!",
            "description": f"Date: **{opex_date.strftime('%B %d, %Y')}**",
            "color": 0xFF9900,  # Orange - Warning
            "fields": [
                {
                    "name": "📊 Action Required",
                    "value": "Time to review your positions",
                    "inline": False
                },
                {
                    "name": "⏰ Time Until Expiration",
                    "value": "Expiration in ~24 hours at market close",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = "⚠️ **OPEX ALERT** - Tomorrow is options expiration day!"
        return self.send_message(content, embeds=[embed])
    
    def send_d0_alert(self, opex_date: datetime) -> bool:
        """
        Send a D-0 (day of) alert for OPEX.
        
        Args:
            opex_date: The OPEX date (today)
            
        Returns:
            True if successful, False otherwise
        """
        embed = {
            "title": "🚨 TODAY IS OPEX!",
            "description": f"Date: **{opex_date.strftime('%B %d, %Y')}**",
            "color": 0xFF0000,  # Red - Urgent
            "fields": [
                {
                    "name": "📈 Market Status",
                    "value": "Market is NOW OPEN",
                    "inline": True
                },
                {
                    "name": "⏰ Expiration Time",
                    "value": "4:00 PM ET (Market Close)",
                    "inline": True
                },
                {
                    "name": "🚨 Critical Reminder",
                    "value": "Options expire at market close today!",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = "🚨 **URGENT: TODAY IS OPEX** - Options expire at market close!"
        return self.send_message(content, embeds=[embed])


def get_next_opex(opex_dates: List[datetime]) -> Optional[datetime]:
    """
    Get the next upcoming OPEX date.
    
    Args:
        opex_dates: List of OPEX dates
        
    Returns:
        The next OPEX date or None if all dates have passed
    """
    today = datetime.now()
    for opex_date in opex_dates:
        if opex_date.date() >= today.date():
            return opex_date
    return None


def check_opex_in_week(opex_dates: List[datetime]) -> Optional[datetime]:
    """
    Check if there's an OPEX date in the next 7 days (including today).
    
    Args:
        opex_dates: List of OPEX dates
        
    Returns:
        The OPEX date if one exists in next 7 days, None otherwise
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    for opex_date in opex_dates:
        if today <= opex_date.date() <= next_week:
            return opex_date
    return None


def check_opex_tomorrow(opex_dates: List[datetime]) -> Optional[datetime]:
    """
    Check if tomorrow is an OPEX date.
    
    Args:
        opex_dates: List of OPEX dates
        
    Returns:
        The OPEX date if tomorrow is OPEX, None otherwise
    """
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    for opex_date in opex_dates:
        if opex_date.date() == tomorrow:
            return opex_date
    return None


def check_opex_today(opex_dates: List[datetime]) -> Optional[datetime]:
    """
    Check if today is an OPEX date.
    
    Args:
        opex_dates: List of OPEX dates
        
    Returns:
        The OPEX date if today is OPEX, None otherwise
    """
    today = datetime.now().date()
    
    for opex_date in opex_dates:
        if opex_date.date() == today:
            return opex_date
    return None


def main():
    """Main function to send OPEX alerts."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send OPEX alerts to Discord')
    parser.add_argument(
        '--alert-type',
        type=str,
        choices=['weekly', 'd1', 'd0', 'calendar'],
        default='calendar',
        help='Type of alert to send: weekly (week preview), d1 (day before), d0 (day of), calendar (full calendar)'
    )
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not set")
        print("Please create a .env file with your Discord webhook URL")
        sys.exit(1)
    
    # Initialize Discord webhook
    discord = DiscordWebhook(webhook_url)
    
    # Calculate OPEX dates for 2026
    year = 2026
    opex_dates = OPEXCalculator.get_opex_dates_for_year(year)
    
    # Handle different alert types
    if args.alert_type == 'weekly':
        # Weekly preview - check if OPEX in next 7 days
        opex_date = check_opex_in_week(opex_dates)
        if opex_date:
            today = datetime.now().date()
            days_until = (opex_date.date() - today).days
            print(f"Sending weekly preview for OPEX on {opex_date.strftime('%B %d, %Y')} ({days_until} days)...")
            if discord.send_weekly_preview(opex_date, days_until):
                print("✓ Weekly preview sent successfully")
            else:
                print("✗ Failed to send weekly preview")
                sys.exit(1)
        else:
            print("No OPEX in the next 7 days - no alert sent")
    
    elif args.alert_type == 'd1':
        # D-1 alert - check if tomorrow is OPEX
        opex_date = check_opex_tomorrow(opex_dates)
        if opex_date:
            print(f"Sending D-1 alert for OPEX tomorrow {opex_date.strftime('%B %d, %Y')}...")
            if discord.send_d1_alert(opex_date):
                print("✓ D-1 alert sent successfully")
            else:
                print("✗ Failed to send D-1 alert")
                sys.exit(1)
        else:
            print("Tomorrow is not an OPEX date - no alert sent")
    
    elif args.alert_type == 'd0':
        # D-0 alert - check if today is OPEX
        opex_date = check_opex_today(opex_dates)
        if opex_date:
            print(f"Sending D-0 alert for OPEX today {opex_date.strftime('%B %d, %Y')}...")
            if discord.send_d0_alert(opex_date):
                print("✓ D-0 alert sent successfully")
            else:
                print("✗ Failed to send D-0 alert")
                sys.exit(1)
        else:
            print("Today is not an OPEX date - no alert sent")
    
    else:  # calendar
        # Send full calendar and next OPEX alert (original behavior)
        print(f"Sending OPEX calendar for {year}...")
        if discord.send_opex_calendar(year, opex_dates):
            print("✓ OPEX calendar sent successfully")
        else:
            print("✗ Failed to send OPEX calendar")
            sys.exit(1)
        
        # Find and alert on next OPEX
        next_opex = get_next_opex(opex_dates)
        if next_opex:
            today = datetime.now()
            days_until = (next_opex.date() - today.date()).days
            
            print(f"\nSending alert for next OPEX...")
            if discord.send_opex_alert(next_opex, days_until):
                print(f"✓ Alert sent for OPEX on {next_opex.strftime('%B %d, %Y')} ({days_until} days)")
            else:
                print("✗ Failed to send OPEX alert")
                sys.exit(1)
        else:
            print("\nNo upcoming OPEX dates found for 2026")


if __name__ == "__main__":
    main()