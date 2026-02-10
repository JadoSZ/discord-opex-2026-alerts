"""
Test Discord Webhook

Simple script to test Discord webhook delivery.
Can read webhook URL from environment variable or command-line argument.
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv


def send_test_message(webhook_url: str) -> bool:
    """
    Send a test message to Discord webhook.
    
    Args:
        webhook_url: The Discord webhook URL
        
    Returns:
        True if successful, False otherwise
    """
    embed = {
        "title": "🧪 Webhook Test",
        "description": "This is a test message to verify webhook connectivity",
        "color": 0x00FF00,  # Green color
        "fields": [
            {
                "name": "Status",
                "value": "✓ Connection successful",
                "inline": True
            },
            {
                "name": "Timestamp",
                "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "inline": True
            }
        ],
        "footer": {
            "text": "OPEX Alerts Test"
        }
    }
    
    payload = {
        "content": "✅ Test message from OPEX Alerts system",
        "embeds": [embed]
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending test message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False


def main():
    """Main function to test webhook."""
    # Load environment variables
    load_dotenv()
    
    # Check for webhook URL in arguments or environment
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
        print("Using webhook URL from command line argument")
    else:
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if webhook_url:
            print("Using webhook URL from environment variable")
        else:
            print("❌ Error: No webhook URL provided")
            print("\nUsage:")
            print("  python test_webhook.py <webhook_url>")
            print("  OR")
            print("  Set DISCORD_WEBHOOK_URL in .env file and run: python test_webhook.py")
            sys.exit(1)
    
    # Validate webhook URL format
    if not webhook_url.startswith('https://discord.com/api/webhooks/'):
        print("⚠️  Warning: URL doesn't appear to be a Discord webhook URL")
        print(f"Expected format: https://discord.com/api/webhooks/...")
        print(f"Got: {webhook_url[:50]}...")
    
    print(f"\n📡 Sending test message to Discord...")
    
    if send_test_message(webhook_url):
        print("✅ SUCCESS: Test message delivered successfully!")
        print("Check your Discord channel to confirm the message was received.")
        sys.exit(0)
    else:
        print("❌ FAILED: Could not deliver test message")
        print("Please check your webhook URL and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
