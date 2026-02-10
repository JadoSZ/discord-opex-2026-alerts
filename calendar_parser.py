"""
OPEX Calendar Parser Module
Extracts OPEX dates from PDF calendar file
"""

import PyPDF2
from datetime import datetime
import re
from typing import List, Optional


class OPEXCalendarParser:
    """Parser for OPEX calendar PDF files"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.opex_dates = []
        
    def parse_calendar(self) -> List[datetime]:
        """
        Parse the PDF calendar and extract OPEX dates
        Returns a list of datetime objects representing OPEX dates
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Parse dates from text
                self.opex_dates = self._extract_dates(text)
                return self.opex_dates
                
        except FileNotFoundError:
            print(f"Error: Calendar file not found at {self.pdf_path}")
            return []
        except Exception as e:
            print(f"Error parsing calendar: {e}")
            return []
    
    def _extract_dates(self, text: str) -> List[datetime]:
        """
        Extract OPEX dates from text
        Common patterns: MM/DD/YYYY, Month DD YYYY, etc.
        """
        dates = []
        
        # Pattern 1: MM/DD/YYYY
        pattern1 = r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b'
        matches1 = re.findall(pattern1, text)
        for match in matches1:
            try:
                date = datetime(int(match[2]), int(match[0]), int(match[1]))
                if date.year == 2026:  # Filter for 2026
                    dates.append(date)
            except ValueError:
                continue
        
        # Pattern 2: Month DD, YYYY (e.g., "January 16, 2026")
        pattern2 = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        for match in matches2:
            try:
                date = datetime.strptime(f"{match[0]} {match[1]} {match[2]}", "%B %d %Y")
                if date.year == 2026:
                    dates.append(date)
            except ValueError:
                continue
        
        # Remove duplicates and sort
        dates = list(set(dates))
        dates.sort()
        
        return dates
    
    def get_next_opex_date(self, from_date: Optional[datetime] = None) -> Optional[datetime]:
        """Get the next OPEX date from the given date (or today if not specified)"""
        if not self.opex_dates:
            return None
            
        if from_date is None:
            from_date = datetime.now()
        
        for date in self.opex_dates:
            if date.date() >= from_date.date():
                return date
        
        return None
    
    def get_opex_dates_in_week(self, start_date: datetime) -> List[datetime]:
        """Get all OPEX dates in the week starting from start_date"""
        from datetime import timedelta
        
        end_date = start_date + timedelta(days=7)
        
        return [date for date in self.opex_dates 
                if start_date.date() <= date.date() < end_date.date()]
