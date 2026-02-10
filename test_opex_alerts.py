"""
Unit tests for OPEX calculator
"""

import unittest
from datetime import datetime
from opex_alerts import OPEXCalculator, get_next_opex


class TestOPEXCalculator(unittest.TestCase):
    """Test cases for OPEX date calculations."""
    
    def test_third_friday_january_2026(self):
        """Test that January 2026 OPEX is January 16."""
        opex_date = OPEXCalculator.get_third_friday(2026, 1)
        self.assertEqual(opex_date.day, 16)
        self.assertEqual(opex_date.month, 1)
        self.assertEqual(opex_date.year, 2026)
        self.assertEqual(opex_date.weekday(), 4)  # Friday
    
    def test_third_friday_february_2026(self):
        """Test that February 2026 OPEX is February 20."""
        opex_date = OPEXCalculator.get_third_friday(2026, 2)
        self.assertEqual(opex_date.day, 20)
        self.assertEqual(opex_date.month, 2)
        self.assertEqual(opex_date.year, 2026)
        self.assertEqual(opex_date.weekday(), 4)  # Friday
    
    def test_third_friday_march_2026(self):
        """Test that March 2026 OPEX is March 20."""
        opex_date = OPEXCalculator.get_third_friday(2026, 3)
        self.assertEqual(opex_date.day, 20)
        self.assertEqual(opex_date.month, 3)
        self.assertEqual(opex_date.year, 2026)
        self.assertEqual(opex_date.weekday(), 4)  # Friday
    
    def test_all_opex_dates_are_fridays(self):
        """Test that all OPEX dates in 2026 are Fridays."""
        opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
        for opex_date in opex_dates:
            self.assertEqual(opex_date.weekday(), 4, 
                           f"{opex_date.strftime('%B %d, %Y')} is not a Friday")
    
    def test_opex_dates_count(self):
        """Test that we get 12 OPEX dates for the year."""
        opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
        self.assertEqual(len(opex_dates), 12)
    
    def test_opex_dates_order(self):
        """Test that OPEX dates are in chronological order."""
        opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
        for i in range(len(opex_dates) - 1):
            self.assertLess(opex_dates[i], opex_dates[i + 1])
    
    def test_specific_2026_dates(self):
        """Test specific known OPEX dates for 2026."""
        expected_dates = [
            (1, 16),   # January
            (2, 20),   # February
            (3, 20),   # March
            (4, 17),   # April
            (5, 15),   # May
            (6, 19),   # June
            (7, 17),   # July
            (8, 21),   # August
            (9, 18),   # September
            (10, 16),  # October
            (11, 20),  # November
            (12, 18),  # December
        ]
        
        opex_dates = OPEXCalculator.get_opex_dates_for_year(2026)
        
        for i, (month, day) in enumerate(expected_dates):
            self.assertEqual(opex_dates[i].month, month)
            self.assertEqual(opex_dates[i].day, day)
    
    def test_get_next_opex_with_future_dates(self):
        """Test getting next OPEX when dates are in the future."""
        # Create some test dates in the far future
        test_dates = [
            datetime(2027, 1, 15),
            datetime(2027, 2, 19),
            datetime(2027, 3, 19),
        ]
        
        next_opex = get_next_opex(test_dates)
        # Should return the first date if all are in the future
        self.assertIsNotNone(next_opex)
        self.assertEqual(next_opex, test_dates[0])
    
    def test_get_next_opex_with_mixed_dates(self):
        """Test getting next OPEX with some past and some future dates."""
        # Create dates with some in past and some in future
        test_dates = [
            datetime(2020, 1, 17),  # Past
            datetime(2027, 2, 19),  # Future
            datetime(2027, 3, 19),  # Future
        ]
        
        next_opex = get_next_opex(test_dates)
        # Should return the first future date
        self.assertIsNotNone(next_opex)
        self.assertEqual(next_opex, test_dates[1])
    
    def test_get_next_opex_with_past_dates(self):
        """Test getting next OPEX when all dates are in the past."""
        # Create dates in the past
        test_dates = [
            datetime(2020, 1, 17),
            datetime(2020, 2, 21),
            datetime(2020, 3, 20),
        ]
        
        next_opex = get_next_opex(test_dates)
        # Should return None when all dates have passed
        self.assertIsNone(next_opex)
    
    def test_check_opex_in_week_with_upcoming(self):
        """Test checking for OPEX in next 7 days when one exists."""
        from opex_alerts import check_opex_in_week
        from datetime import timedelta
        
        # Create dates with one in 5 days
        today = datetime.now()
        test_dates = [
            today + timedelta(days=5),
            today + timedelta(days=15),
            today + timedelta(days=25),
        ]
        
        opex_in_week = check_opex_in_week(test_dates)
        self.assertIsNotNone(opex_in_week)
        self.assertEqual(opex_in_week, test_dates[0])
    
    def test_check_opex_in_week_with_none(self):
        """Test checking for OPEX in next 7 days when none exists."""
        from opex_alerts import check_opex_in_week
        from datetime import timedelta
        
        # Create dates all beyond 7 days
        today = datetime.now()
        test_dates = [
            today + timedelta(days=15),
            today + timedelta(days=25),
            today + timedelta(days=35),
        ]
        
        opex_in_week = check_opex_in_week(test_dates)
        self.assertIsNone(opex_in_week)
    
    def test_check_opex_tomorrow_with_match(self):
        """Test checking if tomorrow is OPEX when it is."""
        from opex_alerts import check_opex_tomorrow
        from datetime import timedelta
        
        # Create date for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        test_dates = [
            tomorrow,
            datetime.now() + timedelta(days=5),
        ]
        
        opex_tomorrow = check_opex_tomorrow(test_dates)
        self.assertIsNotNone(opex_tomorrow)
        self.assertEqual(opex_tomorrow.date(), tomorrow.date())
    
    def test_check_opex_tomorrow_with_no_match(self):
        """Test checking if tomorrow is OPEX when it's not."""
        from opex_alerts import check_opex_tomorrow
        from datetime import timedelta
        
        # Create dates that don't include tomorrow
        test_dates = [
            datetime.now() + timedelta(days=5),
            datetime.now() + timedelta(days=15),
        ]
        
        opex_tomorrow = check_opex_tomorrow(test_dates)
        self.assertIsNone(opex_tomorrow)
    
    def test_check_opex_today_with_match(self):
        """Test checking if today is OPEX when it is."""
        from opex_alerts import check_opex_today
        from datetime import timedelta
        
        # Create date for today
        today = datetime.now()
        test_dates = [
            today,
            datetime.now() + timedelta(days=5),
        ]
        
        opex_today = check_opex_today(test_dates)
        self.assertIsNotNone(opex_today)
        self.assertEqual(opex_today.date(), today.date())
    
    def test_check_opex_today_with_no_match(self):
        """Test checking if today is OPEX when it's not."""
        from opex_alerts import check_opex_today
        from datetime import timedelta
        
        # Create dates that don't include today
        test_dates = [
            datetime.now() + timedelta(days=5),
            datetime.now() + timedelta(days=15),
        ]
        
        opex_today = check_opex_today(test_dates)
        self.assertIsNone(opex_today)


class TestDiscordWebhook(unittest.TestCase):
    """Test cases for Discord webhook functionality."""
    
    def test_webhook_initialization(self):
        """Test that webhook can be initialized with URL."""
        from opex_alerts import DiscordWebhook
        webhook_url = "https://discord.com/api/webhooks/test/test"
        webhook = DiscordWebhook(webhook_url)
        self.assertEqual(webhook.webhook_url, webhook_url)


if __name__ == '__main__':
    unittest.main()
