"""
Script to create a sample OPEX calendar PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from datetime import datetime


def create_sample_opex_calendar():
    """Create a sample OPEX calendar PDF for 2026"""
    
    # Standard OPEX dates for 2026 (Third Friday of each month)
    opex_dates_2026 = [
        "January 16, 2026",
        "February 20, 2026",
        "March 20, 2026",
        "April 17, 2026",
        "May 15, 2026",
        "June 19, 2026",
        "July 17, 2026",
        "August 21, 2026",
        "September 18, 2026",
        "October 16, 2026",
        "November 20, 2026",
        "December 18, 2026",
    ]
    
    filename = "opex_calendar.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("<b>2026 OPEX Calendar</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Description
    desc = Paragraph("Monthly Options Expiration Dates (Third Friday)", styles['Normal'])
    story.append(desc)
    story.append(Spacer(1, 20))
    
    # Create table data
    data = [['Month', 'OPEX Date']]
    for date_str in opex_dates_2026:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        month = date_obj.strftime("%B")
        data.append([month, date_str])
    
    # Create table
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    print(f"Sample OPEX calendar created: {filename}")


if __name__ == '__main__':
    create_sample_opex_calendar()
