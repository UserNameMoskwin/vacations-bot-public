"""
Google Sheets API module - reads absence data from spreadsheet.
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from typing import List, Dict, Optional

from config import SPREADSHEET_ID, GOOGLE_APPLICATION_CREDENTIALS, SHEET_NAME

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def get_sheets_service():
    """Create and return Google Sheets API service."""
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS,
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in DD.MM.YYYY format."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), '%d.%m.%Y')
    except ValueError:
        return None


def fetch_absences() -> List[Dict]:
    """
    Fetch absence records from Google Sheets.

    Returns list of dictionaries with keys:
    - type: str (Vacation, Sick, Other)
    - employee: str
    - start: datetime
    - end: datetime
    - working_days: int
    - calendar_days: int
    """
    sheets = get_sheets_service()

    # Read data from the sheet
    range_name = f'{SHEET_NAME}!A:F'
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()

    values = result.get('values', [])

    if not values or len(values) < 2:
        return []

    # Skip header row
    records = []
    for row in values[1:]:
        if len(row) < 6:
            continue

        absence_type = row[0].strip() if row[0] else ''
        employee = row[1].strip() if row[1] else ''
        start_date = parse_date(row[2]) if row[2] else None
        end_date = parse_date(row[3]) if row[3] else None

        # Parse numeric fields
        try:
            working_days = int(row[4]) if row[4] else 0
        except ValueError:
            working_days = 0

        try:
            calendar_days = int(row[5]) if row[5] else 0
        except ValueError:
            calendar_days = 0

        # Skip invalid records
        if not all([absence_type, employee, start_date, end_date]):
            continue

        records.append({
            'type': absence_type,
            'employee': employee,
            'start': start_date,
            'end': end_date,
            'working_days': working_days,
            'calendar_days': calendar_days
        })

    return records
