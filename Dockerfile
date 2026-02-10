FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py .
COPY calendar_parser.py .
COPY opex_calendar.pdf .

# Create .env file placeholder
RUN touch .env

CMD ["python", "bot.py"]
