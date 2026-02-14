"""
Unit tests for OPEX Alerts system
"""

import unittest
from datetime import datetime, timedelta
from opex_alerts import (
    OPEXCalendar, 
    OPEXCalculator,
    get_events_for_alerts,
    adjust_alert_for_weekend
)


class TestOPEXCalendar(unittest.TestCase):
    """Test OPEXCalendar class"""
    
    def setUp(self):
        """Set up test calendar"""
        self.calendar = OPEXCalendar('calendar_2026.json')
    
    def test_calendar_loads(self):
        """Test that calendar loads successfully"""
        self.assertIsNotNone(self.calendar.data)
        self.assertEqual(self.calendar.data.get('year'), 2026)
    
    def test_exchange_holidays_count(self):
        """Test that all 10 exchange holidays are loaded"""
        holidays = self.calendar.get_events_by_type('exchange_holidays')
        self.assertEqual(len(holidays), 10)
    
    def test_standard_expirations_count(self):
        """Test that all 12 standard expirations are loaded"""
        expirations = self.calendar.get_events_by_type('standard_expirations')
        self.assertEqual(len(expirations), 12)
    
    def test_vix_expirations_count(self):
        """Test that all 12 VIX expirations are loaded"""
        vix_exp = self.calendar.get_events_by_type('vix_standard_expirations')
        self.assertEqual(len(vix_exp), 12)
    
    def test_am_settled_count(self):
        """Test that all 12 AM-settled last trading days are loaded"""
        am_settled = self.calendar.get_events_by_type('am_settled_last_trading_days')
        self.assertEqual(len(am_settled), 12)
    
    def test_eom_quarter_count(self):
        """Test that all 4 end-of-quarter expirations are loaded"""
        eom = self.calendar.get_events_by_type('end_of_month_quarter')
        self.assertEqual(len(eom), 4)
    
    def test_leaps_count(self):
        """Test that all 3 LEAPS additions are loaded"""
        leaps = self.calendar.get_events_by_type('leaps_additions')
        self.assertEqual(len(leaps), 3)
    
    def test_june_irregular_date(self):
        """Test that June 18 (Thursday) is correctly marked as irregular"""
        expirations = self.calendar.get_events_by_type('standard_expirations')
        june_events = [e for e in expirations if '2026-06' in e['date']]
        
        self.assertEqual(len(june_events), 1)
        self.assertEqual(june_events[0]['date'], '2026-06-18')
        self.assertEqual(june_events[0]['day_of_week'], 'Thursday')
        self.assertIn('Juneteenth', june_events[0]['notes'])
    
    def test_frequency_low(self):
        """Test low frequency includes correct event types"""
        events = self.calendar.get_all_events_by_frequency('low')
        # Low should have 12 standard + 4 quarterly = 16 events
        self.assertEqual(len(events), 16)
    
    def test_frequency_medium(self):
        """Test medium frequency includes correct event types"""
        events = self.calendar.get_all_events_by_frequency('medium')
        # Medium: 12 standard + 12 VIX + 4 quarterly + 3 LEAPS + 10 holidays = 41
        self.assertEqual(len(events), 41)
    
    def test_frequency_high(self):
        """Test high frequency includes correct event types"""
        events = self.calendar.get_all_events_by_frequency('high')
        # High: 12 standard + 12 VIX + 12 AM-settled + 4 quarterly + 3 LEAPS + 10 holidays = 53
        self.assertEqual(len(events), 53)
    
    def test_get_next_event(self):
        """Test getting next event from a specific date"""
        # Test from January 1, 2026
        test_date = datetime(2026, 1, 1)
        next_event = self.calendar.get_next_event(test_date, 'medium')
        
        self.assertIsNotNone(next_event)
        event_date = datetime.fromisoformat(next_event['date'])
        self.assertGreaterEqual(event_date.date(), test_date.date())
    
    def test_get_events_in_range(self):
        """Test getting events within a date range"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 31)
        
        events = self.calendar.get_events_in_date_range(start, end, 'medium')
        
        # Should find events in January
        self.assertGreater(len(events), 0)
        
        # All events should be in January
        for event in events:
            event_date = datetime.fromisoformat(event['date'])
            self.assertGreaterEqual(event_date, start)
            self.assertLessEqual(event_date, end)


class TestOPEXCalculator(unittest.TestCase):
    """Test OPEXCalculator class (backward compatibility)"""
    
    def test_2026_dates_count(self):
        """Test that 2026 has 12 OPEX dates"""
        dates = OPEXCalculator.get_opex_dates_for_year(2026)
        self.assertEqual(len(dates), 12)
    
    def test_specific_2026_dates(self):
        """Test specific 2026 dates including irregular June date"""
        dates = OPEXCalculator.get_opex_dates_for_year(2026)
        
        # Check January
        self.assertEqual(dates[0].month, 1)
        self.assertEqual(dates[0].day, 16)
        
        # Check June (irregular - Thursday)
        expected_june_date = (6, 18)  # Updated expected date
        june_date = dates[5]
        self.assertEqual((june_date.month, june_date.day), expected_june_date)
        self.assertEqual(june_date.strftime('%A'), 'Thursday')
        
        # Check December
        self.assertEqual(dates[11].month, 12)
        self.assertEqual(dates[11].day, 18)
    
    def test_third_friday_calculation(self):
        """Test third Friday calculation"""
        # Test some known third Fridays
        jan_2026 = OPEXCalculator.get_third_friday(2026, 1)
        self.assertEqual(jan_2026.day, 16)
        self.assertEqual(jan_2026.strftime('%A'), 'Friday')


class TestAlertHelpers(unittest.TestCase):
    """Test alert helper functions"""
    
    def setUp(self):
        """Set up test calendar"""
        self.calendar = OPEXCalendar('calendar_2026.json')
    
    def test_get_events_for_alerts(self):
        """Test getting events for specific days ahead"""
        # This test will depend on current date, so we test the logic
        events_1day = get_events_for_alerts(self.calendar, 1, 'medium')
        self.assertIsInstance(events_1day, list)
        
        events_3days = get_events_for_alerts(self.calendar, 3, 'medium')
        self.assertIsInstance(events_3days, list)
    
    def test_weekend_adjustment_saturday(self):
        """Test that Saturday alerts move to Friday"""
        # Create a Saturday date
        saturday = datetime(2026, 1, 3)  # January 3, 2026 is Saturday
        adjusted = adjust_alert_for_weekend(saturday)
        
        # Should be moved to Friday
        self.assertEqual(adjusted.weekday(), 4)  # Friday
        self.assertEqual(adjusted.day, 2)
    
    def test_weekend_adjustment_sunday(self):
        """Test that Sunday alerts move to Friday"""
        # Create a Sunday date
        sunday = datetime(2026, 1, 4)  # January 4, 2026 is Sunday
        adjusted = adjust_alert_for_weekend(sunday)
        
        # Should be moved to Friday
        self.assertEqual(adjusted.weekday(), 4)  # Friday
        self.assertEqual(adjusted.day, 2)
    
    def test_weekend_adjustment_weekday(self):
        """Test that weekday alerts are not adjusted"""
        # Create a Monday date
        monday = datetime(2026, 1, 5)  # January 5, 2026 is Monday
        adjusted = adjust_alert_for_weekend(monday)
        
        # Should remain unchanged
        self.assertEqual(adjusted, monday)


class TestEventTypes(unittest.TestCase):
    """Test event type specific logic"""
    
    def setUp(self):
        """Set up test calendar"""
        self.calendar = OPEXCalendar('calendar_2026.json')
    
    def test_vix_has_last_trading_day(self):
        """Test that VIX expirations include last trading day"""
        vix_events = self.calendar.get_events_by_type('vix_standard_expirations')
        
        for event in vix_events:
            self.assertIn('last_trading_day', event)
            self.assertIsNotNone(event['last_trading_day'])
    
    def test_am_settled_has_expiration_date(self):
        """Test that AM-settled events include expiration date"""
        am_events = self.calendar.get_events_by_type('am_settled_last_trading_days')
        
        for event in am_events:
            self.assertIn('expiration_date', event)
            self.assertIsNotNone(event['expiration_date'])
    
    def test_leaps_has_year(self):
        """Test that LEAPS additions include year"""
        leaps_events = self.calendar.get_events_by_type('leaps_additions')
        
        for event in leaps_events:
            self.assertIn('leaps_year', event)
            self.assertEqual(event['leaps_year'], 2029)
    
    def test_holidays_have_names(self):
        """Test that holidays include holiday names"""
        holidays = self.calendar.get_events_by_type('exchange_holidays')
        
        for holiday in holidays:
            self.assertIn('name', holiday)
            self.assertIsNotNone(holiday['name'])
            self.assertGreater(len(holiday['name']), 0)
    
    def test_juneteenth_holiday_exists(self):
        """Test that Juneteenth is in the holiday list"""
        holidays = self.calendar.get_events_by_type('exchange_holidays')
        juneteenth = [h for h in holidays if 'Juneteenth' in h['name']]
        
        self.assertEqual(len(juneteenth), 1)
        self.assertEqual(juneteenth[0]['date'], '2026-06-19')
        self.assertEqual(juneteenth[0]['day_of_week'], 'Friday')


if __name__ == '__main__':
    unittest.main()

