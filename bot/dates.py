"""
Date utilities module - handles date calculations and timezone operations.
"""
from datetime import datetime, timedelta
from typing import Tuple
import pytz

from config import TIMEZONE


def get_timezone():
    """Get configured timezone object."""
    return pytz.timezone(TIMEZONE)


def get_today() -> datetime:
    """Get current date in configured timezone (date only, no time)."""
    tz = get_timezone()
    now = datetime.now(tz)
    return datetime(now.year, now.month, now.day)


def is_friday() -> bool:
    """Check if today is Friday (weekday 4)."""
    tz = get_timezone()
    return datetime.now(tz).weekday() == 4


def is_weekday() -> bool:
    """Check if today is a weekday (Monday-Friday)."""
    tz = get_timezone()
    return datetime.now(tz).weekday() < 5


def get_next_week_range() -> Tuple[datetime, datetime]:
    """
    Get the date range for next work week (Monday 00:00 to Friday 23:59).

    Returns:
        Tuple of (monday_start, friday_end) for next week
    """
    today = get_today()

    # Calculate days until next Monday
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, get next Monday

    next_monday = today + timedelta(days=days_until_monday)
    next_friday = next_monday + timedelta(days=4)

    return next_monday, next_friday


def format_date(dt: datetime) -> str:
    """Format datetime as DD.MM.YYYY."""
    return dt.strftime('%d.%m.%Y')
