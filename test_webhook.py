#!/usr/bin/env python3
"""
Simple Discord Webhook Test Script

Sends a test message to verify your Discord webhook is working.
This script will ALWAYS send a message, regardless of dates.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

def send_test_message(webhook_url: str) -> bool:
    """
    Send a test message to Discord.
    
    Args:
        webhook_url: The Discord webhook URL
        
    Returns:
        True if successful, False otherwise
    """
    now = datetime.now()
    
    # All OPEX dates for 2026 (pre-calculated)
    opex_dates = [
        "January 16, 2026 (Friday)",
        "February 20, 2026 (Friday)",
        "March 20, 2026 (Friday)",
        "April 17, 2026 (Friday)",
        "May 15, 2026 (Friday)",
        "June 19, 2026 (Friday)",
        "July 17, 2026 (Friday)",
        "August 21, 2026 (Friday)",
        "September 18, 2026 (Friday)",
        "October 16, 2026 (Friday)",
        "November 20, 2026 (Friday)",
        "December 18, 2026 (Friday)"
    ]
    
    dates_text = "\n".join(f"• {date}" for date in opex_dates)
    
    embed = {
        "title": "✅ Discord Webhook Test",
        "description": "Your Discord webhook is working correctly!",
        "color": 0x00FF00,  # Green
        "fields": [
            {
                "name": "🕐 Test Time",
                "value": now.strftime('%B %d, %Y at %I:%M:%S %p'),
                "inline": False
            },
            {
                "name": "📅 2026 OPEX Dates",
                "value": dates_text,
                "inline": False
            },
            {
                "name": "✨ Status",
                "value": "All systems operational!",
                "inline": False
            }
        ],
        "footer": {
            "text": "OPEX Alert System • Test Message"
        },
        "timestamp": now.isoformat()
    }
    
    payload = {
        "content": "🧪 **Webhook Test** - This is a test message from your OPEX Alert System!",
        "embeds": [embed]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending message to Discord: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False


def main():
    """Main function to test Discord webhook."""
    print("=" * 60)
    print("Discord Webhook Test Script")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("❌ Error: DISCORD_WEBHOOK_URL environment variable not set")
        print()
        print("Please ensure your GitHub Secret is configured:")
        print("  1. Go to: Settings > Secrets and variables > Actions")
        print("  2. Add secret: DISCORD_WEBHOOK_URL")
        print("  3. Value: Your Discord webhook URL")
        print()
        sys.exit(1)
    
    print(f"🔗 Webhook URL: {webhook_url[:50]}...")
    print()
    print("📤 Sending test message to Discord...")
    print()
    
    if send_test_message(webhook_url):
        print("✅ SUCCESS! Test message sent to Discord.")
        print()
        print("Check your Discord channel now!")
        print("You should see a green test message with:")
        print("  • Current test time")
        print("  • All 2026 OPEX dates")
        print("  • Success confirmation")
        print()
        sys.exit(0)
    else:
        print("❌ FAILED! Could not send test message.")
        print()
        print("Possible issues:")
        print("  • Webhook URL is incorrect")
        print("  • Webhook was deleted from Discord")
        print("  • Network connection issues")
        print("  • Discord API is down")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
