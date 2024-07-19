from typing import Any, List, Dict
from datetime import datetime
from googleapiclient.errors import HttpError

def check_if_cal_exists(service: Any, name: str) -> Any:
    existing_calendars = service.calendarList().list().execute()
    for calendar_entry in existing_calendars.get('items', []):
        if calendar_entry.get('summary') == name:
            return calendar_entry
    return None

def create_calendar(service: Any, data_dict: Dict[str, Any]) -> Any:
    # Calendar details
    calendar_summary: str = data_dict.get('course code', 'NA')
    calendar_description: str = data_dict.get('course name', 'NA')

    # Check if a calendar with the same summary already exists
    calendar_entry: Any = check_if_cal_exists(service, calendar_summary)
    calendar_id = calendar_entry.get('id') if calendar_entry else None
    if calendar_id is not None:
        print(f"Found existing calendar: {calendar_summary}, clearing its events.")
        clear_calendar_events(service, calendar_id)
        return calendar_entry

    # Create the calendar if it does not exist
    calendar: Dict[str, str] = {
        'summary': calendar_summary,
        'description': calendar_description
    }
    created_calendar: Any = service.calendars().insert(body=calendar).execute()
    print(f"Created calendar: {created_calendar['summary']}")
    return created_calendar

def clear_calendar_events(service: Any, calendar_id: str) -> None:
    events = service.events().list(calendarId=calendar_id).execute().get('items', [])
    for event in events:
        try:
            service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
            print(f"Deleted event: {event['summary']}")
        except HttpError as error:
            print(f"Error deleting event {event['summary']}: {error}")

def make_dict_for_time(start: Dict[str, str], end: Dict[str, str]) -> Dict[str, Any]:
    start_date: str = f"{start.get('date', '')} {start.get('time', '')}".strip()
    end_date: str = f"{end.get('date', '')} {end.get('time', '')}".strip()
    if ' ' not in start_date or ' ' not in end_date:
        if end_date == '':
            end_date = start_date
        return {
            'start': {
            'date': start_date,
            },
            'end': {
                'date': end_date,
            }
        }
    else:
        return {
            'start': {
            'dateTime': datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').isoformat() + '-06:00',
            'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').isoformat() + '-06:00',
                'timeZone': 'America/Edmonton',
            },
        }

def create_events(data_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    print(data_dict)
    new_events: List[Dict[str, Any]] = []
    # Event details
    course_name: str = data_dict.get('course name', 'NA')
    course_code: str = data_dict.get('course code', 'NA')
    events: List[Dict[str, Any]] = data_dict.get('events', [])

    for event in events:
        summary: str = f"{course_code} {event.get('name', '')}"
        location: str = event.get('location', 'TBD')
        description: str = event.get('description', 'TBD')
        dates: List[Dict[str, Any]] = event.get('dates', [])

        for date in dates:
            new_event = {
                'summary': summary,
                'location': location,
                'description': description,
                'reminders': {
                    'useDefault': True,
                },
            }
            print(date.get('start', ''))
            new_event.update(make_dict_for_time(date.get('start', {}),
                date.get('end', {})))
            new_event_start = new_event.get('start')
            print(new_event_start)
            if new_event_start is not None:
                if new_event_start.get('date') != '':
                    new_events.append(new_event)
    return new_events

def add_events(service: Any,
    calendar: Any,
    events: List[Dict[str, Any]]) -> None:
    calendar_id: str = calendar['id']

    # Iterate through the events list and insert each event individually
    for event in events:
        try:
            print(f'Inserting event: {event}')
            event_result: Any = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f'Event created: {event_result.get("htmlLink")}')
        except HttpError as error:
            print(f'Error inserting event {event.get("summary")}: {error}')

def make_calendar(service, data_dict: Dict[str, Any]) -> None:
    calendar: Any = create_calendar(service, data_dict)
    events: List[Dict[str, Any]] = create_events(data_dict)
    add_events(service, calendar, events)
