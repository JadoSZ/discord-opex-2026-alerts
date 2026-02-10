"""
Discord OPEX 2026 Alerts

This module calculates OPEX (Options Expiration) dates for 2026 and sends alerts to Discord.
OPEX typically occurs on the third Friday of each month.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv


class OPEXCalculator:
    """Calculate OPEX dates for a given year."""
    
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
        
        Args:
            year: The year to calculate OPEX dates for
            
        Returns:
            List of datetime objects for each OPEX date
        """
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
        
        embed = {
            "title": f"📊 OPEX Calendar {year}",
            "description": f"All options expiration dates for {year} (Third Friday of each month)",
            "color": 0x3498DB,  # Blue color
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📆 OPEX Calendar for {year}"
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


def main():
    """Main function to send OPEX alerts."""
    # Load environment variables
    load_dotenv()
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not set")
        print("Please create a .env file with your Discord webhook URL")
        return
    
    # Initialize Discord webhook
    discord = DiscordWebhook(webhook_url)
    
    # Calculate OPEX dates for 2026
    year = 2026
    opex_dates = OPEXCalculator.get_opex_dates_for_year(year)
    
    print(f"Sending OPEX calendar for {year}...")
    if discord.send_opex_calendar(year, opex_dates):
        print("✓ OPEX calendar sent successfully")
    else:
        print("✗ Failed to send OPEX calendar")
    
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
    else:
        print("\nNo upcoming OPEX dates found for 2026")


if __name__ == "__main__":
    main()
