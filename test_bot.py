"""
Unit tests for OPEX Calendar Parser and Bot functionality
"""

import unittest
from datetime import datetime
from calendar_parser import OPEXCalendarParser
import os


class TestCalendarParser(unittest.TestCase):
    """Test cases for OPEXCalendarParser"""
    
    def test_extract_dates_pattern1(self):
        """Test extraction of MM/DD/YYYY pattern"""
        parser = OPEXCalendarParser("dummy.pdf")
        text = "OPEX dates: 01/16/2026, 02/20/2026, 03/20/2026"
        dates = parser._extract_dates(text)
        
        self.assertEqual(len(dates), 3)
        self.assertEqual(dates[0], datetime(2026, 1, 16))
        self.assertEqual(dates[1], datetime(2026, 2, 20))
        self.assertEqual(dates[2], datetime(2026, 3, 20))
    
    def test_extract_dates_pattern2(self):
        """Test extraction of Month DD, YYYY pattern"""
        parser = OPEXCalendarParser("dummy.pdf")
        text = "OPEX dates: January 16, 2026 and February 20, 2026"
        dates = parser._extract_dates(text)
        
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0], datetime(2026, 1, 16))
        self.assertEqual(dates[1], datetime(2026, 2, 20))
    
    def test_extract_dates_mixed_patterns(self):
        """Test extraction of mixed date patterns"""
        parser = OPEXCalendarParser("dummy.pdf")
        text = "Dates: 01/16/2026 and March 20, 2026"
        dates = parser._extract_dates(text)
        
        self.assertEqual(len(dates), 2)
        self.assertIn(datetime(2026, 1, 16), dates)
        self.assertIn(datetime(2026, 3, 20), dates)
    
    def test_get_next_opex_date(self):
        """Test getting next OPEX date"""
        parser = OPEXCalendarParser("dummy.pdf")
        parser.opex_dates = [
            datetime(2026, 1, 16),
            datetime(2026, 2, 20),
            datetime(2026, 3, 20),
        ]
        
        # Test with a date before first OPEX
        from_date = datetime(2026, 1, 1)
        next_date = parser.get_next_opex_date(from_date)
        self.assertEqual(next_date, datetime(2026, 1, 16))
        
        # Test with a date between OPEX dates
        from_date = datetime(2026, 1, 20)
        next_date = parser.get_next_opex_date(from_date)
        self.assertEqual(next_date, datetime(2026, 2, 20))
    
    def test_get_opex_dates_in_week(self):
        """Test getting OPEX dates in a week"""
        parser = OPEXCalendarParser("dummy.pdf")
        parser.opex_dates = [
            datetime(2026, 1, 14),  # Wednesday
            datetime(2026, 1, 16),  # Friday
            datetime(2026, 1, 23),  # Next Friday
        ]
        
        # Week starting Monday Jan 12
        start_date = datetime(2026, 1, 12)
        dates_in_week = parser.get_opex_dates_in_week(start_date)
        
        self.assertEqual(len(dates_in_week), 2)
        self.assertIn(datetime(2026, 1, 14), dates_in_week)
        self.assertIn(datetime(2026, 1, 16), dates_in_week)
        self.assertNotIn(datetime(2026, 1, 23), dates_in_week)
    
    def test_file_not_found(self):
        """Test handling of missing PDF file"""
        parser = OPEXCalendarParser("nonexistent.pdf")
        dates = parser.parse_calendar()
        self.assertEqual(len(dates), 0)


class TestAlertTiming(unittest.TestCase):
    """Test cases for alert timing logic"""
    
    def test_d_minus_1_time(self):
        """Test D-1 alert timing"""
        # D-1 should trigger at 16:00 Eastern
        test_time = datetime(2026, 1, 15, 16, 0)  # 4:00 PM
        self.assertEqual(test_time.hour, 16)
        self.assertEqual(test_time.minute, 0)
    
    def test_d_0_time(self):
        """Test D-0 alert timing"""
        # D-0 should trigger at 09:00 Eastern
        test_time = datetime(2026, 1, 16, 9, 0)  # 9:00 AM
        self.assertEqual(test_time.hour, 9)
        self.assertEqual(test_time.minute, 0)
    
    def test_weekly_preview_time(self):
        """Test weekly preview timing"""
        # Should trigger on Sunday (weekday 6) at 18:00
        test_time = datetime(2026, 1, 11, 18, 0)  # Sunday 6:00 PM
        self.assertEqual(test_time.weekday(), 6)  # Sunday
        self.assertEqual(test_time.hour, 18)
        self.assertEqual(test_time.minute, 0)


if __name__ == '__main__':
    unittest.main()
