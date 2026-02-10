"""
Script to create a comprehensive OPEX calendar PDF for testing
Includes all events from CBOE 2026 Options Calendar
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime


def create_sample_opex_calendar():
    """Create a comprehensive OPEX calendar PDF for 2026 based on CBOE calendar"""
    
    # Monthly Equity/Index/ETF Options Expiration (Third Friday, or Thursday if holiday)
    monthly_opex_dates = [
        ("January 16, 2026", "Friday"),
        ("February 20, 2026", "Friday"),
        ("March 20, 2026", "Friday"),
        ("April 17, 2026", "Friday"),
        ("May 15, 2026", "Friday"),
        ("June 18, 2026", "Thursday (Juneteenth)"),
        ("July 17, 2026", "Friday"),
        ("August 21, 2026", "Friday"),
        ("September 18, 2026", "Friday"),
        ("October 16, 2026", "Friday"),
        ("November 20, 2026", "Friday"),
        ("December 18, 2026", "Friday"),
    ]
    
    # VIX Options Expiration (Wednesdays, 30 days before monthly SPX expiration)
    vix_opex_dates = [
        ("January 21, 2026", "Wednesday"),
        ("February 18, 2026", "Wednesday"),
        ("March 18, 2026", "Wednesday"),
        ("April 15, 2026", "Wednesday"),
        ("May 19, 2026", "Tuesday (Holiday adjusted)"),
        ("June 17, 2026", "Wednesday"),
        ("July 22, 2026", "Wednesday"),
        ("August 19, 2026", "Wednesday"),
        ("September 16, 2026", "Wednesday"),
        ("October 21, 2026", "Wednesday"),
        ("November 18, 2026", "Wednesday"),
        ("December 16, 2026", "Wednesday"),
    ]
    
    # Market Holidays & Early Closes
    holidays = [
        ("January 1, 2026", "New Year's Day", "CLOSED"),
        ("January 19, 2026", "Martin Luther King Jr. Day", "CLOSED"),
        ("February 16, 2026", "Presidents' Day", "CLOSED"),
        ("April 3, 2026", "Good Friday", "CLOSED"),
        ("May 25, 2026", "Memorial Day", "CLOSED"),
        ("June 19, 2026", "Juneteenth", "CLOSED"),
        ("July 3, 2026", "Independence Day (Observed)", "CLOSED"),
        ("September 7, 2026", "Labor Day", "CLOSED"),
        ("November 26, 2026", "Thanksgiving Day", "CLOSED"),
        ("November 27, 2026", "Day After Thanksgiving", "EARLY CLOSE 1:00 PM ET"),
        ("December 24, 2026", "Christmas Eve", "EARLY CLOSE 1:00 PM ET"),
        ("December 25, 2026", "Christmas Day", "CLOSED"),
    ]
    
    # Special Weekly Expirations (Thursday expirations due to holidays)
    special_weekly = [
        ("April 2, 2026", "Thursday (Good Friday holiday)"),
        ("July 2, 2026", "Thursday (July 4 holiday)"),
        ("December 24, 2026", "Thursday (Christmas holiday)"),
        ("December 31, 2026", "Thursday (New Year holiday)"),
    ]
    
    filename = "opex_calendar_comprehensive.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # ===== TITLE PAGE =====
    title = Paragraph("<b>2026 CBOE Options Expiration Calendar</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    subtitle = Paragraph("<i>Comprehensive Event Calendar including Monthly OPEX, VIX Expiration, Holidays, and Special Events</i>", styles['Normal'])
    story.append(subtitle)
    story.append(Spacer(1, 30))
    
    # ===== MONTHLY OPTIONS EXPIRATION =====
    section1 = Paragraph("<b>Monthly Options Expiration (Equity/Index/ETF)</b>", styles['Heading2'])
    story.append(section1)
    story.append(Spacer(1, 12))
    
    data1 = [['Date', 'Day', 'Month']]
    for date_str, day in monthly_opex_dates:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        month = date_obj.strftime("%B")
        data1.append([date_str, day, month])
    
    table1 = Table(data1, colWidths=[150, 180, 100])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003B5C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F4F8')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    story.append(table1)
    story.append(Spacer(1, 30))
    
    # ===== VIX OPTIONS EXPIRATION =====
    section2 = Paragraph("<b>VIX Options Expiration</b>", styles['Heading2'])
    story.append(section2)
    story.append(Spacer(1, 12))
    
    data2 = [['Date', 'Day', 'Month']]
    for date_str, day in vix_opex_dates:
        date_obj = datetime.strptime(date_str.split(' (')[0], "%B %d, %Y")
        month = date_obj.strftime("%B")
        data2.append([date_str, day, month])
    
    table2 = Table(data2, colWidths=[180, 180, 100])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFE4E1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    story.append(table2)
    story.append(PageBreak())
    
    # ===== MARKET HOLIDAYS =====
    section3 = Paragraph("<b>Market Holidays & Early Closes</b>", styles['Heading2'])
    story.append(section3)
    story.append(Spacer(1, 12))
    
    data3 = [['Date', 'Holiday', 'Status']]
    for date_str, holiday, status in holidays:
        data3.append([date_str, holiday, status])
    
    table3 = Table(data3, colWidths=[120, 220, 140])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F4F4F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5DC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    story.append(table3)
    story.append(Spacer(1, 30))
    
    # ===== SPECIAL WEEKLY EXPIRATIONS =====
    section4 = Paragraph("<b>Special Weekly Expirations (Holiday Adjusted)</b>", styles['Heading2'])
    story.append(section4)
    story.append(Spacer(1, 12))
    
    data4 = [['Date', 'Notes']]
    for date_str, note in special_weekly:
        data4.append([date_str, note])
    
    table4 = Table(data4, colWidths=[150, 310])
    table4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF8C00')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFEFD5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    
    story.append(table4)
    story.append(Spacer(1, 30))
    
    # ===== FOOTER NOTES =====
    notes = Paragraph("<b>Notes:</b><br/>• Monthly options expire on the third Friday of each month (or Thursday if Friday is a holiday)<br/>• VIX options typically expire 30 days before the following month's standard expiration<br/>• LEAPS expire in January (equity) and December/January/June (index)<br/>• Quarterly expirations: March, June, September, December<br/>• Source: CBOE 2026 Options Calendar", styles['Normal'])
    story.append(notes)
    
    # Build PDF
    doc.build(story)
    print(f"Comprehensive OPEX calendar created: {filename}")


if __name__ == '__main__':
    create_sample_opex_calendar()