"""
Main bot module - entry point for generating reports.
"""
import sys
import io
import json

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import validate_config
from sheets import fetch_absences
from logic import get_report_data
from formatter import format_report


def generate_report() -> str:
    """
    Generate the absence report.

    Returns:
        Formatted report string
    """
    # Validate configuration
    validate_config()

    # Fetch data from Google Sheets
    records = fetch_absences()

    # Process data
    report_data = get_report_data(records)

    # Format message
    message = format_report(report_data)

    return message


def main():
    """
    Main entry point.

    When called from Node.js, outputs JSON with the report.
    """
    try:
        report = generate_report()
        result = {
            'success': True,
            'message': report
        }
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }

    # Output JSON for Node.js to parse
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
