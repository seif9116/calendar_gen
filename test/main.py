from utils import get_service, CALENDAR_SCOPES, SHEET_SCOPES
from get_events import create_client, get_events
from make_calendar import make_calendar
from typing import Dict, Any, List

def get_sheet_title() -> str:
    return 'Spring 2024 Due Dates'

def make_spreadsheet(service: Any, data_dict: Dict[str, Any]) -> None:
    sheet_title = get_sheet_title()

    # Check if a spreadsheet with the same title already exists
    response = service.spreadsheets().get(spreadsheetId='spreadsheetId').execute()
    existing_sheets = response.get('sheets', [])

    spreadsheet_id = None
    for sheet in existing_sheets:
        if sheet.get('properties', {}).get('title', '') == sheet_title:
            spreadsheet_id = response.get('spreadsheetId')
            break

    if spreadsheet_id:
        # Check if headers are the same
        range = 'A1:F1'
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
        existing_headers = result.get('values', [])

        new_headers = [['Class', 'Date', 'Type', 'Weight', 'Due in', 'Done']]
        if existing_headers != new_headers:
            # Clear existing headers and add new ones
            body = {
                'values': new_headers
            }
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range,
                valueInputOption='RAW',
                body=body
            ).execute()
            print('Headers updated')
        else:
            print('Headers are already up to date')
    else:
        # Create a new spreadsheet
        spreadsheet = {
            'properties': {
                'title': sheet_title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId', '')
        print(f'Spreadsheet ID: {spreadsheet_id}')

        # Define the header row
        header = [['Class', 'Date', 'Type', 'Weight', 'Due in', 'Done']]

        # Write the header to the spreadsheet
        range = 'A1:F1'
        value_input_option = 'RAW'
        body = {
            'values': header
        }

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption=value_input_option,
            body=body
        ).execute()
        print('Spreadsheet created and header added')

def main() -> None:
    # Step 1: Get the data from pdf
    data_dict: Dict[str, Any] = get_events('input')

    # Step 2: Turn it into a calendar
    '''
    calendar_service: Any = get_service("calendar",
        "v3",
        CALENDAR_SCOPES,
        "token_calendar.json",
        5000)
    make_calendar(calendar_service, data_dict)
    '''
    # Step 3: Turn it into a spreadsheet
    sheets_service: Any = get_service("sheets",
        "v4",
        SHEET_SCOPES,
        "token_sheets.json",
        5001)
    make_spreadsheet(sheets_service, data_dict)

if __name__ == '__main__':
    main()
