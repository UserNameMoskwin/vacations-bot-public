"""
Message formatter module - formats absence data into Telegram messages.
"""
from typing import List, Dict
from collections import defaultdict

from dates import format_date

# Emoji and labels for absence types
TYPE_CONFIG = {
    'Vacation': {'emoji': '🏖', 'label': 'Vacation'},
    'Sick': {'emoji': '🤒', 'label': 'Sick Leave'},
    'Other': {'emoji': '📋', 'label': 'Other'}
}


def format_absence_line(record: Dict) -> str:
    """
    Format a single absence record as a line.
    """
    start_str = format_date(record['start'])
    end_str = format_date(record['end'])
    days = record['calendar_days']

    return f"    • {record['employee']}\n      {start_str} – {end_str} ({days} days)"


def group_by_type(records: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group records by absence type.
    """
    grouped = defaultdict(list)
    for record in records:
        grouped[record['type']].append(record)
    return grouped


def format_grouped_section(title: str, title_emoji: str, records: List[Dict]) -> str:
    """
    Format a section with title and records grouped by type.
    """
    if not records:
        return ""

    lines = [f"{title_emoji} <b>{title}</b>"]
    grouped = group_by_type(records)

    # Order: Vacation, Sick, Other
    for absence_type in ['Vacation', 'Sick', 'Other']:
        type_records = grouped.get(absence_type, [])
        if type_records:
            config = TYPE_CONFIG[absence_type]
            lines.append(f"\n{config['emoji']} <i>{config['label']}</i>")
            for record in type_records:
                lines.append(format_absence_line(record))

    return '\n'.join(lines)


def format_report(data: Dict) -> str:
    """
    Format the full report message with HTML formatting for Telegram.
    """
    sections = []

    # Header
    header = "🌴 <b>Absence Report</b>"
    sections.append(header)

    # Combine today's absences
    today_all = data['today_vacations'] + data['today_other']
    today_section = format_grouped_section("Today", "📅", today_all)
    if today_section:
        sections.append(today_section)

    # Next week sections (only on Friday)
    if data['is_friday']:
        next_week_all = data['next_week_vacations'] + data['next_week_other']
        next_week_section = format_grouped_section("Next Week", "📆", next_week_all)
        if next_week_section:
            sections.append(next_week_section)

    # Check if only header exists (no absences)
    if len(sections) == 1:
        sections.append("✅ Everyone is present today!")

    return '\n\n'.join(sections)
