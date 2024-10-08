from utils import get_service, CALENDAR_SCOPES, SHEET_SCOPES, DRIVE_SCOPES
from get_events import create_client, get_events
from make_calendar import make_calendar
from typing import Dict, Any, List

def get_sheet_title() -> str:
    return 'Spring 2024 Due Dates'

def check_spreadsheet_exists(service: Any, sheet_title: str) -> str | None:
    # Use the Drive API to search for the spreadsheet by name
    query = f"name = '{sheet_title}' and mimeType = 'application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, spaces='drive').execute()

    files = results.get('files', [])

    if files:
        return files[0].get('id')  # Return the ID of the first matching spreadsheet
    else:
        return None

def make_headers(sheet_service: Any, spreadsheet_id: str) -> None:
    # Check if headers are the same
    range = 'A1:F1'
    result = sheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    existing_headers = result.get('values', [])

    new_headers = [['Class', 'Date', 'Type', 'Weight', 'Due in', 'Done']]
    if existing_headers != new_headers:
        # Clear existing headers and add new ones
        body = {
            'values': new_headers
        }
        sheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='RAW',
            body=body
        ).execute()
        print('Headers updated')
    else:
        print('Headers are already up to date')

def make_spreadsheet(sheet_service: Any,
    drive_service: Any,
    data_dict: Dict[str, Any]) -> None:

    sheet_title = get_sheet_title()

    spreadsheet_id : str | None = check_spreadsheet_exists(drive_service, sheet_title)
    if spreadsheet_id:
        make_headers(sheet_service, spreadsheet_id)
    else:
        # Create a new spreadsheet
        spreadsheet = {
            'properties': {
                'title': sheet_title
            }
        }
        spreadsheet = sheet_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        spreadsheet_id: str | None = spreadsheet.get('spreadsheetId', '')
        print(f'Spreadsheet ID: {spreadsheet_id}')

        if spreadsheet_id:
            make_headers(sheet_service, spreadsheet_id)
            print('Spreadsheet created and header added')
    events: List[Dict[str, Any]] = data_dict.get('events', [])
    class_name = data_dict.get('course code', '')

    new_headers = [['Class', 'Date', 'Type', 'Weight', 'Due in', 'Done']]
    for event in events:
        type: str = event.get('EventType', '')
        weight: Dict[str, Any] = event.get('weight', {})
        dates = event.get('dates', [])
        weight_value: int = weight.get('value', 0) / len(dates)

        for date in dates:
            ...

def fill_row()

def main() -> None:
    # Step 1: Get the data from pdf
    data_dict: Dict[str, Any] = get_events('input')
    print(data_dict)

    # Step 2: Turn it into a calendar
    calendar_service: Any = get_service("calendar",
        "v3",
        CALENDAR_SCOPES,
        "token_calendar.json",
        5000)
    make_calendar(calendar_service, data_dict)
    # Step 3: Turn it into a spreadsheet
    #drive_service: Any = get_service("drive",
    #    "v3",
    #    DRIVE_SCOPES,
    #    "token_drive.json",
    #    5002)
    #sheets_service: Any = get_service("sheets",
    #    "v4",
    #    SHEET_SCOPES,
    #    "token_sheets.json",
    #   5001)
    # make_spreadsheet(sheets_service, drive_service, data_dict)

if __name__ == '__main__':
    main()
