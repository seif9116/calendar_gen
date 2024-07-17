from utils import get_service, CALENDAR_SCOPES, SHEET_SCOPES
from get_events import create_client, get_events
from make_calendar import make_calendar
from typing import Dict, Any, List

def get_sheet_title() -> str:
    return 'Spring 2024 Due Dates'

def make_spreadsheet(service: Any, data_dict: Dict[str, Any]) -> None:
    spreadsheet: Dict[str, Any] = {
        'properties': {
            'title': get_sheet_title()
        }
    }
    spreadsheet: Dict[str, Any] = service.spreadsheets().create(body=spreadsheet,
        fields='spreadsheetId').execute()

    spreadsheet_id: str = spreadsheet.get('spreadsheetId', '')
    print(f'Spreadsheet ID: {spreadsheet_id}')

    # Define the header row
    header: List[List[str]] = [['Class', 'Date', 'Type', 'Weight', 'Due in', 'Done']]

    # Write the header to the spreadsheet
    range: str = 'A1:F1'
    value_input_option: str = 'RAW'
    body: Dict[str, Any] = {
        'values': header
    }

    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption=value_input_option,
        body=body).execute()
    print('Spreadsheet created and header added')

def main() -> None:
    # Step 1: Get the data from pdf
    data_dict: Dict[str, Any] = get_events('input')

    # Step 2: Turn it into a calendar
    calendar_service: Any = get_service("calendar",
        "v3",
        CALENDAR_SCOPES,
        "token_calendar.json",
        5000)
    make_calendar(calendar_service, data_dict)

    # Step 3: Turn it into a spreadsheet
    sheets_service: Any = get_service("sheets",
        "v4",
        SHEET_SCOPES,
        "token_sheets.json",
        5001)
    make_spreadsheet(sheets_service, data_dict)

if __name__ == '__main__':
    main()
