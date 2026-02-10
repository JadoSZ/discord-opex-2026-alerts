# Updated opex_alerts.py

import datetime

# Accurate CBOE 2026 dates with holiday adjustments
# The third Friday of June is actually June 18 for this year
OPEX_DATES_2026 = {
    'January': '2026-01-21',
    'February': '2026-02-20',
    'March': '2026-03-20',
    'April': '2026-04-17',
    'May': '2026-05-15',
    'June': '2026-06-18',  # Adjusted from 19 to 18
    'July': '2026-07-17',
    'August': '2026-08-21',
    'September': '2026-09-18',
    'October': '2026-10-16',
    'November': '2026-11-20',
    'December': '2026-12-18',
}


def get_vix_opex_dates_for_year(year):
    # This method will return a hardcoded list of VIX expiry dates for the CBOE 2026 calendar 
    return [
        '2026-01-21',
        '2026-02-20',
        '2026-03-20',
        '2026-04-17',
        '2026-05-15',
        '2026-06-18',
        '2026-07-17',
        '2026-08-21',
        '2026-09-18',
        '2026-10-16',
        '2026-11-20',
        '2026-12-18'
    ]


def send_vix_opex_alert(date):
    # Logic to send alert for the specific VIX expiration date
    print(f"VIX OPEX alert for date: {date}")


# Example of how to call the new methods
if __name__ == '__main__':
    vix_dates = get_vix_opex_dates_for_year(2026)
    for date in vix_dates:
        send_vix_opex_alert(date)