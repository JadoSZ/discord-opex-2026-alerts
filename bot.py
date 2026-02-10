"""
Discord OPEX Alerts Bot
Automates OPEX alerts for a Discord channel
"""

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from calendar_parser import OPEXCalendarParser
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))
CALENDAR_PDF_PATH = os.getenv('CALENDAR_PDF_PATH', 'opex_calendar.pdf')

# Timezone
EASTERN = pytz.timezone('US/Eastern')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Global calendar parser
calendar_parser = None


@bot.event
async def on_ready():
    """Called when bot is ready"""
    global calendar_parser
    logger.info(f'{bot.user} has connected to Discord!')
    
    # Initialize calendar parser
    calendar_parser = OPEXCalendarParser(CALENDAR_PDF_PATH)
    calendar_parser.parse_calendar()
    logger.info(f'Loaded {len(calendar_parser.opex_dates)} OPEX dates from calendar')
    
    # Start scheduled tasks
    if not d_minus_1_alert.is_running():
        d_minus_1_alert.start()
    if not d_0_alert.is_running():
        d_0_alert.start()
    if not weekly_preview.is_running():
        weekly_preview.start()
    
    logger.info('All scheduled tasks started')


@tasks.loop(minutes=1)
async def d_minus_1_alert():
    """
    D-1 Alert: Send alert one day before OPEX at 16:00 PM Eastern
    """
    now = datetime.now(EASTERN)
    
    # Check if it's 16:00 PM Eastern (4:00 PM)
    if now.hour == 16 and now.minute == 0:
        tomorrow = now + timedelta(days=1)
        
        # Check if tomorrow is an OPEX date
        if calendar_parser:
            next_opex = calendar_parser.get_next_opex_date(tomorrow)
            
            if next_opex and next_opex.date() == tomorrow.date():
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    embed = discord.Embed(
                        title="🔔 OPEX Alert - D-1",
                        description=f"**Options Expiration Tomorrow!**",
                        color=discord.Color.orange(),
                        timestamp=datetime.now(pytz.UTC)
                    )
                    embed.add_field(
                        name="OPEX Date",
                        value=next_opex.strftime("%A, %B %d, %Y"),
                        inline=False
                    )
                    embed.add_field(
                        name="Time Remaining",
                        value="Approximately 17 hours until market open",
                        inline=False
                    )
                    embed.set_footer(text="Automated OPEX Alert System")
                    
                    await channel.send(embed=embed)
                    logger.info(f'Sent D-1 alert for {next_opex.date()}')


@tasks.loop(minutes=1)
async def d_0_alert():
    """
    D-0 Alert: Send alert on OPEX day at 09:00 AM Eastern
    """
    now = datetime.now(EASTERN)
    
    # Check if it's 09:00 AM Eastern
    if now.hour == 9 and now.minute == 0:
        today = now
        
        # Check if today is an OPEX date
        if calendar_parser:
            opex_dates = [d for d in calendar_parser.opex_dates if d.date() == today.date()]
            
            if opex_dates:
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    embed = discord.Embed(
                        title="🚨 OPEX Alert - TODAY",
                        description=f"**Options Expiration Day!**",
                        color=discord.Color.red(),
                        timestamp=datetime.now(pytz.UTC)
                    )
                    embed.add_field(
                        name="OPEX Date",
                        value=today.strftime("%A, %B %d, %Y"),
                        inline=False
                    )
                    embed.add_field(
                        name="Market Status",
                        value="Market is now open - OPEX day in progress",
                        inline=False
                    )
                    embed.set_footer(text="Automated OPEX Alert System")
                    
                    await channel.send(embed=embed)
                    logger.info(f'Sent D-0 alert for {today.date()}')


@tasks.loop(minutes=1)
async def weekly_preview():
    """
    Weekly Preview: Send preview every Sunday at 18:00 PM Eastern if there's an event
    """
    now = datetime.now(EASTERN)
    
    # Check if it's Sunday (weekday 6) at 18:00 PM
    if now.weekday() == 6 and now.hour == 18 and now.minute == 0:
        
        # Get OPEX dates for the upcoming week
        if calendar_parser:
            upcoming_dates = calendar_parser.get_opex_dates_in_week(now)
            
            if upcoming_dates:
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    embed = discord.Embed(
                        title="📅 Weekly OPEX Preview",
                        description=f"**Upcoming OPEX Events This Week**",
                        color=discord.Color.blue(),
                        timestamp=datetime.now(pytz.UTC)
                    )
                    
                    for i, date in enumerate(upcoming_dates, 1):
                        days_until = (date.date() - now.date()).days
                        embed.add_field(
                            name=f"OPEX Event #{i}",
                            value=f"{date.strftime('%A, %B %d, %Y')}\n({days_until} days away)",
                            inline=False
                        )
                    
                    embed.set_footer(text="Automated OPEX Alert System")
                    
                    await channel.send(embed=embed)
                    logger.info(f'Sent weekly preview with {len(upcoming_dates)} upcoming OPEX dates')


@bot.command(name='nextopex')
async def next_opex(ctx):
    """Command to check the next OPEX date"""
    if calendar_parser:
        next_date = calendar_parser.get_next_opex_date()
        if next_date:
            days_until = (next_date.date() - datetime.now().date()).days
            await ctx.send(f"📅 Next OPEX: {next_date.strftime('%A, %B %d, %Y')} ({days_until} days away)")
        else:
            await ctx.send("No upcoming OPEX dates found in the calendar.")
    else:
        await ctx.send("Calendar not loaded. Please check the PDF file.")


@bot.command(name='listopex')
async def list_opex(ctx):
    """Command to list all OPEX dates"""
    if calendar_parser and calendar_parser.opex_dates:
        embed = discord.Embed(
            title="📋 All OPEX Dates for 2026",
            color=discord.Color.green()
        )
        
        # Group by month
        from collections import defaultdict
        dates_by_month = defaultdict(list)
        for date in calendar_parser.opex_dates:
            dates_by_month[date.strftime('%B %Y')].append(date)
        
        for month, dates in sorted(dates_by_month.items()):
            dates_str = '\n'.join([d.strftime('%A, %B %d') for d in sorted(dates)])
            embed.add_field(name=month, value=dates_str, inline=True)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("No OPEX dates found in the calendar.")


@bot.command(name='reload')
@commands.has_permissions(administrator=True)
async def reload_calendar(ctx):
    """Admin command to reload the calendar"""
    global calendar_parser
    calendar_parser = OPEXCalendarParser(CALENDAR_PDF_PATH)
    calendar_parser.parse_calendar()
    await ctx.send(f"✅ Calendar reloaded! Found {len(calendar_parser.opex_dates)} OPEX dates.")


def main():
    """Main entry point"""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        return
    
    if not CHANNEL_ID:
        logger.error("CHANNEL_ID not found in environment variables")
        return
    
    logger.info("Starting Discord OPEX Alerts Bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
