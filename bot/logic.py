"""
Business logic module - filters absences by date criteria.
"""
from datetime import datetime
from typing import List, Dict, Tuple

from dates import get_today, get_next_week_range, is_friday


def is_active_today(record: Dict, today: datetime) -> bool:
    """
    Check if absence record is active today.

    Criteria: Start <= today <= End
    """
    return record['start'] <= today <= record['end']


def intersects_next_week(record: Dict, week_start: datetime, week_end: datetime) -> bool:
    """
    Check if absence record intersects with next week.

    Criteria:
    - Start <= week_end AND End >= week_start

    This covers cases where absence:
    - Starts and ends within the week
    - Starts before and continues into the week
    - Starts in the week and ends after
    - Completely covers the week
    """
    return record['start'] <= week_end and record['end'] >= week_start


def filter_absences_today(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Filter absences that are active today.

    Returns:
        Tuple of (vacations, other_absences)
        - vacations: records with type "Vacation"
        - other_absences: records with type "Sick" or "Other"
    """
    today = get_today()

    vacations = []
    other_absences = []

    for record in records:
        if is_active_today(record, today):
            if record['type'] == 'Vacation':
                vacations.append(record)
            else:
                other_absences.append(record)

    return vacations, other_absences


def filter_absences_next_week(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """
    Filter absences that intersect with next week.
    Only used on Fridays.

    Returns:
        Tuple of (vacations, other_absences)
        - vacations: records with type "Vacation"
        - other_absences: records with type "Sick" or "Other"
    """
    week_start, week_end = get_next_week_range()

    vacations = []
    other_absences = []

    for record in records:
        if intersects_next_week(record, week_start, week_end):
            if record['type'] == 'Vacation':
                vacations.append(record)
            else:
                other_absences.append(record)

    return vacations, other_absences


def get_report_data(records: List[Dict]) -> Dict:
    """
    Get all data needed for the report.

    Returns dictionary with:
    - today_vacations: List[Dict]
    - today_other: List[Dict]
    - next_week_vacations: List[Dict] (only on Friday)
    - next_week_other: List[Dict] (only on Friday)
    - is_friday: bool
    """
    today_vacations, today_other = filter_absences_today(records)

    result = {
        'today_vacations': today_vacations,
        'today_other': today_other,
        'is_friday': is_friday()
    }

    if is_friday():
        next_week_vacations, next_week_other = filter_absences_next_week(records)
        result['next_week_vacations'] = next_week_vacations
        result['next_week_other'] = next_week_other
    else:
        result['next_week_vacations'] = []
        result['next_week_other'] = []

    return result
