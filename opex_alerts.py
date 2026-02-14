"""
Discord OPEX 2026 Alerts

This module provides OPEX (Options Expiration) dates for 2026 and sends alerts to Discord.
Uses official CBOE 2026 calendar with holiday adjustments.
Supports multiple event types and alert frequency levels.
"""

import os
import sys
import argparse
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv


class OPEXCalendar:
    """Manage comprehensive OPEX calendar data for 2026 with all event types."""
    
    def __init__(self, calendar_path: str = "calendar_2026.json"):
        """
        Initialize calendar from JSON file.
        
        Args:
            calendar_path: Path to calendar JSON file
        """
        self.calendar_path = calendar_path
        self.data = {}
        self.load_calendar()
    
    def load_calendar(self):
        """Load calendar data from JSON file."""
        try:
            with open(self.calendar_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Calendar file not found at {self.calendar_path}")
            self.data = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing calendar JSON: {e}")
            self.data = {}
    
    def get_events_by_type(self, event_type: str) -> List[Dict]:
        """
        Get all events of a specific type.
        
        Args:
            event_type: Type of event (e.g., 'standard_expirations', 'vix_standard_expirations')
        
        Returns:
            List of event dictionaries
        """
        return self.data.get(event_type, [])
    
    def get_all_events_by_frequency(self, frequency: str = "medium") -> List[Dict]:
        """
        Get all events based on frequency level.
        
        Args:
            frequency: Alert frequency level ('low', 'medium', 'high')
        
        Returns:
            List of all events with their types
        """
        freq_config = self.data.get("alert_frequencies", {}).get(frequency, {})
        includes = freq_config.get("includes", [])
        
        all_events = []
        for event_type in includes:
            events = self.get_events_by_type(event_type)
            for event in events:
                event_copy = event.copy()
                event_copy['event_type'] = event_type
                all_events.append(event_copy)
        
        # Sort by date
        all_events.sort(key=lambda x: datetime.fromisoformat(x['date']))
        return all_events
    
    def get_events_in_date_range(self, start_date: datetime, end_date: datetime, 
                                  frequency: str = "medium") -> List[Dict]:
        """
        Get events within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            frequency: Alert frequency level
        
        Returns:
            List of events in the date range
        """
        all_events = self.get_all_events_by_frequency(frequency)
        filtered = []
        
        for event in all_events:
            event_date = datetime.fromisoformat(event['date'])
            if start_date.date() <= event_date.date() <= end_date.date():
                filtered.append(event)
        
        return filtered
    
    def get_next_event(self, from_date: Optional[datetime] = None, 
                       frequency: str = "medium") -> Optional[Dict]:
        """
        Get the next upcoming event.
        
        Args:
            from_date: Date to search from (default: today)
            frequency: Alert frequency level
        
        Returns:
            Next event dictionary or None
        """
        if from_date is None:
            from_date = datetime.now()
        
        all_events = self.get_all_events_by_frequency(frequency)
        
        for event in all_events:
            event_date = datetime.fromisoformat(event['date'])
            if event_date.date() >= from_date.date():
                return event
        
        return None


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
    """Handle Discord webhook notifications with support for multiple event types."""
    
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
    
    def send_event_alert(self, event: Dict, days_until: int) -> bool:
        """
        Send an alert for any event type based on the event data.
        
        Args:
            event: Event dictionary from calendar
            days_until: Days until the event
        
        Returns:
            True if successful, False otherwise
        """
        event_type = event.get('event_type', 'unknown')
        event_date = datetime.fromisoformat(event['date'])
        
        # Determine alert format based on event type
        if event_type == 'standard_expirations':
            return self._send_standard_expiration_alert(event, event_date, days_until)
        elif event_type == 'vix_standard_expirations':
            return self._send_vix_expiration_alert(event, event_date, days_until)
        elif event_type == 'am_settled_last_trading_days':
            return self._send_am_settled_alert(event, event_date, days_until)
        elif event_type == 'end_of_month_quarter':
            return self._send_eom_quarter_alert(event, event_date, days_until)
        elif event_type == 'leaps_additions':
            return self._send_leaps_alert(event, event_date, days_until)
        elif event_type == 'exchange_holidays':
            return self._send_holiday_alert(event, event_date, days_until)
        else:
            # Generic alert
            return self._send_generic_alert(event, event_date, days_until)
    
    def _send_standard_expiration_alert(self, event: Dict, event_date: datetime, 
                                        days_until: int) -> bool:
        """Send alert for standard options expiration."""
        notes = event.get('notes', '')
        details = f"\n{notes}" if notes else ""
        
        embed = {
            "title": "📅 **Upcoming Standard Options Expiration**",
            "description": f"**Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Type:** {event.get('type', 'Options Expiration')}"
                          f"{details}",
            "color": 0xFF9900,  # Orange
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                },
                {
                    "name": "Day of Week",
                    "value": event_date.strftime('%A'),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📅 **Standard Options Expiration in {days_until} day{'s' if days_until != 1 else ''}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_vix_expiration_alert(self, event: Dict, event_date: datetime, 
                                   days_until: int) -> bool:
        """Send alert for VIX options expiration."""
        last_trading_day = event.get('last_trading_day', '')
        if last_trading_day:
            ltd_date = datetime.fromisoformat(last_trading_day)
            ltd_str = ltd_date.strftime('%A, %B %d, %Y')
        else:
            ltd_str = "N/A"
        
        notes = event.get('notes', '')
        details = f"\n{notes}" if notes else ""
        
        embed = {
            "title": "📊 **Upcoming VIX Options Expiration**",
            "description": f"**Expiration Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Last Trading Day:** {ltd_str}"
                          f"{details}",
            "color": 0x3498DB,  # Blue
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📊 **VIX Options Expiration in {days_until} day{'s' if days_until != 1 else ''}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_am_settled_alert(self, event: Dict, event_date: datetime, 
                               days_until: int) -> bool:
        """Send alert for AM-settled index last trading day."""
        expiration_date = event.get('expiration_date', '')
        if expiration_date:
            exp_date = datetime.fromisoformat(expiration_date)
            exp_str = exp_date.strftime('%A, %B %d, %Y')
        else:
            exp_str = "N/A"
        
        notes = event.get('notes', '')
        details = f"\n{notes}" if notes else ""
        
        embed = {
            "title": "⏰ **Last Day to Trade AM-Settled Index Options**",
            "description": f"**Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Expiration Tomorrow:** {exp_str}"
                          f"{details}",
            "color": 0xFF5733,  # Red-Orange
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"⏰ **Last Day to Trade AM-Settled Options in {days_until} day{'s' if days_until != 1 else ''}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_eom_quarter_alert(self, event: Dict, event_date: datetime, 
                                days_until: int) -> bool:
        """Send alert for end-of-month/quarter expiration."""
        event_period = event.get('type', 'Month')
        notes = event.get('notes', '')
        details = f" - {notes}" if notes else ""
        
        embed = {
            "title": f"📆 **End-of-{event_period} Options Expiration**",
            "description": f"**Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Type:** {event_period} End Options{details}",
            "color": 0x9B59B6,  # Purple
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📆 **End-of-{event_period} Expiration in {days_until} day{'s' if days_until != 1 else ''}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_leaps_alert(self, event: Dict, event_date: datetime, 
                         days_until: int) -> bool:
        """Send alert for LEAPS addition."""
        leaps_year = event.get('leaps_year', '2029')
        notes = event.get('notes', '')
        
        embed = {
            "title": f"🆕 **{leaps_year} LEAPS Series Added**",
            "description": f"**Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Details:** {notes}",
            "color": 0x2ECC71,  # Green
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"🆕 **{leaps_year} LEAPS Addition in {days_until} day{'s' if days_until != 1 else ''}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_holiday_alert(self, event: Dict, event_date: datetime, 
                           days_until: int) -> bool:
        """Send alert for exchange holiday."""
        holiday_name = event.get('name', 'Market Holiday')
        
        embed = {
            "title": "🏦 **Exchange Holiday - Market Closed**",
            "description": f"**Date:** {event_date.strftime('%A, %B %d, %Y')}\n"
                          f"**Holiday:** {holiday_name}",
            "color": 0xE74C3C,  # Red
            "fields": [
                {
                    "name": "⏰ Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"🏦 **Market Holiday in {days_until} day{'s' if days_until != 1 else ''}: {holiday_name}**"
        return self.send_message(content, embeds=[embed])
    
    def _send_generic_alert(self, event: Dict, event_date: datetime, 
                           days_until: int) -> bool:
        """Send generic alert for unknown event types."""
        embed = {
            "title": "📅 Event Alert",
            "description": f"Date: **{event_date.strftime('%A, %B %d, %Y')}**",
            "color": 0x95A5A6,  # Gray
            "fields": [
                {
                    "name": "Days Until",
                    "value": str(days_until),
                    "inline": True
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        content = f"📅 Event in {days_until} day{'s' if days_until != 1 else ''}"
        return self.send_message(content, embeds=[embed])
    
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


def get_events_for_alerts(calendar: OPEXCalendar, days_ahead: int, 
                          frequency: str = "medium") -> List[Dict]:
    """
    Get events that need alerts for a specific number of days ahead.
    
    Args:
        calendar: OPEXCalendar instance
        days_ahead: Number of days ahead to check (1, 2, or 3)
        frequency: Alert frequency level
    
    Returns:
        List of events occurring in days_ahead days
    """
    target_date = datetime.now() + timedelta(days=days_ahead)
    
    # Get events for just that specific day
    events = calendar.get_events_in_date_range(target_date, target_date, frequency)
    
    return events


def adjust_alert_for_weekend(alert_date: datetime) -> datetime:
    """
    Adjust alert date if it falls on a weekend.
    If alert would be on Saturday or Sunday, move to Friday.
    
    Args:
        alert_date: The intended alert date
    
    Returns:
        Adjusted date (Friday if weekend, otherwise unchanged)
    """
    weekday = alert_date.weekday()
    
    # If Saturday (5), move back 1 day to Friday
    if weekday == 5:
        return alert_date - timedelta(days=1)
    # If Sunday (6), move back 2 days to Friday
    elif weekday == 6:
        return alert_date - timedelta(days=2)
    
    return alert_date


def main():
    """Main function to send OPEX alerts."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send OPEX alerts to Discord')
    parser.add_argument(
        '--alert-type',
        type=str,
        choices=['weekly', 'd1', 'd2', 'd3', 'd0', 'calendar', 'test'],
        default='calendar',
        help='Type of alert to send: weekly (week preview), d1/d2/d3 (1-3 days before), d0 (day of), calendar (full calendar), test (test all formats)'
    )
    parser.add_argument(
        '--frequency',
        type=str,
        choices=['low', 'medium', 'high'],
        default='medium',
        help='Alert frequency level: low (monthly+quarterly), medium (standard), high (all events)'
    )
    parser.add_argument(
        '--calendar-file',
        type=str,
        default='calendar_2026.json',
        help='Path to calendar JSON file'
    )
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL environment variable not set")
        print("Please create a .env file with your Discord webhook URL")
        sys.exit(1)
    
    # Initialize Discord webhook and calendar
    discord = DiscordWebhook(webhook_url)
    calendar = OPEXCalendar(args.calendar_file)
    
    if not calendar.data:
        print("Error: Could not load calendar data")
        sys.exit(1)
    
    # Handle different alert types
    if args.alert_type in ['d1', 'd2', 'd3']:
        # D-1, D-2, D-3 alerts - check for events N days ahead
        days_ahead = int(args.alert_type[1])
        events = get_events_for_alerts(calendar, days_ahead, args.frequency)
        
        if events:
            print(f"Sending D-{days_ahead} alerts for {len(events)} event(s)...")
            for event in events:
                event_date = datetime.fromisoformat(event['date'])
                if discord.send_event_alert(event, days_ahead):
                    print(f"✓ Alert sent for {event.get('event_type')} on {event_date.strftime('%B %d, %Y')}")
                else:
                    print(f"✗ Failed to send alert for {event_date.strftime('%B %d, %Y')}")
        else:
            print(f"No events {days_ahead} days ahead - no alert sent")
    
    elif args.alert_type == 'd0':
        # D-0 alert - check if today has events
        events = get_events_for_alerts(calendar, 0, args.frequency)
        
        if events:
            print(f"Sending D-0 alerts for {len(events)} event(s) today...")
            for event in events:
                event_date = datetime.fromisoformat(event['date'])
                if discord.send_event_alert(event, 0):
                    print(f"✓ Alert sent for {event.get('event_type')} on {event_date.strftime('%B %d, %Y')}")
                else:
                    print(f"✗ Failed to send alert for {event_date.strftime('%B %d, %Y')}")
        else:
            print("No events today - no alert sent")
    
    elif args.alert_type == 'weekly':
        # Weekly preview - check for events in next 7 days
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        events = calendar.get_events_in_date_range(start_date, end_date, args.frequency)
        
        if events:
            print(f"Sending weekly preview for {len(events)} event(s)...")
            
            # Create a comprehensive weekly preview embed
            embed = {
                "title": "📅 Weekly Preview - Upcoming Events",
                "description": f"Events for the week of {start_date.strftime('%B %d, %Y')}",
                "color": 0x3498DB,  # Blue
                "fields": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            for event in events:
                event_date = datetime.fromisoformat(event['date'])
                days_until = (event_date.date() - start_date.date()).days
                event_type = event.get('event_type', 'event').replace('_', ' ').title()
                
                field_value = f"**{event_date.strftime('%A, %B %d, %Y')}**\n"
                field_value += f"Days until: {days_until}\n"
                
                if event.get('notes'):
                    field_value += f"_{event['notes']}_"
                
                embed["fields"].append({
                    "name": f"{event_type}",
                    "value": field_value,
                    "inline": False
                })
            
            embed["footer"] = {"text": f"Frequency: {args.frequency.capitalize()}"}
            
            content = f"📅 **Weekly Preview** - {len(events)} event(s) upcoming"
            if discord.send_message(content, embeds=[embed]):
                print("✓ Weekly preview sent successfully")
            else:
                print("✗ Failed to send weekly preview")
        else:
            print("No events in the next 7 days - no preview sent")
    
    elif args.alert_type == 'test':
        # Test mode - send one example of each event type
        print("Testing all alert formats...")
        
        event_types = [
            'standard_expirations',
            'vix_standard_expirations',
            'am_settled_last_trading_days',
            'end_of_month_quarter',
            'leaps_additions',
            'exchange_holidays'
        ]
        
        for event_type in event_types:
            events = calendar.get_events_by_type(event_type)
            if events:
                test_event = events[0].copy()
                test_event['event_type'] = event_type
                event_date = datetime.fromisoformat(test_event['date'])
                days_until = (event_date.date() - datetime.now().date()).days
                
                print(f"\nTesting {event_type}...")
                if discord.send_event_alert(test_event, days_until):
                    print(f"✓ Test alert sent for {event_type}")
                else:
                    print(f"✗ Failed to send test alert for {event_type}")
                
                # Small delay between messages
                import time
                time.sleep(2)
    
    else:  # calendar
        # Send full calendar (original behavior for backward compatibility)
        year = calendar.data.get('year', 2026)
        opex_dates = OPEXCalculator.get_opex_dates_for_year(year)
        
        print(f"Sending OPEX calendar for {year}...")
        if discord.send_opex_calendar(year, opex_dates):
            print("✓ OPEX calendar sent successfully")
        else:
            print("✗ Failed to send OPEX calendar")
            sys.exit(1)
        
        # Find and alert on next OPEX
        next_opex_event = calendar.get_next_event(frequency=args.frequency)
        if next_opex_event:
            event_date = datetime.fromisoformat(next_opex_event['date'])
            days_until = (event_date.date() - datetime.now().date()).days
            
            print(f"\nSending alert for next event...")
            if discord.send_event_alert(next_opex_event, days_until):
                print(f"✓ Alert sent for {next_opex_event.get('event_type')} on {event_date.strftime('%B %d, %Y')} ({days_until} days)")
            else:
                print("✗ Failed to send event alert")
        else:
            print("\nNo upcoming events found")


if __name__ == "__main__":
    main()