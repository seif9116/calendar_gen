from typing import Any, List, Dict
from datetime import datetime
from googleapiclient.errors import HttpError

def create_calendar(service: Any, data_dict: Dict[str, Any]) -> Any:
    # Calendar details
    calendar_summary: str = data_dict.get('course code', 'NA')
    calendar_description: str = data_dict.get('course name', 'NA')

    # Check if a calendar with the same summary already exists
    existing_calendars = service.calendarList().list().execute()
    for calendar_entry in existing_calendars.get('items', []):
        if calendar_entry.get('summary') == calendar_summary:
            calendar_id = calendar_entry.get('id')
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

def make_dict_for_time(start: str, end: str) -> Dict[str, Any]:
    if ' ' not in start or ' ' not in end:
        if end == '':
            end = start
        return {
            'start': {
            'date': start,
            },
            'end': {
                'date': end,
            }
        }
    else:
        return {
            'start': {
            'dateTime': datetime.strptime(start, '%Y-%m-%d %H:%M:%S').isoformat() + '-06:00',
            'timeZone': 'America/Edmonton',
            },
            'end': {
                'dateTime': datetime.strptime(end, '%Y-%m-%d %H:%M:%S').isoformat() + '-06:00',
                'timeZone': 'America/Edmonton',
            },
        }

def create_events(data_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    print(data_dict)
    new_events: List[Dict[str, Any]] = []
    # Event details
    course_name: str = data_dict.get('course name', 'NA')
    course_code: str = data_dict.get('course code', 'NA')
    events: List[Dict[str, str]] = data_dict.get('events', [])

    for event in events:
        summary: str = f"{course_code} {event.get('name', '')}"
        location: str = event.get('location', 'TBD')
        description: str = event.get('description', 'TBD')

        new_event = {
            'summary': summary,
            'location': location,
            'description': description,
            'reminders': {
                'useDefault': True,
            },
        }
        new_event.update(make_dict_for_time(event.get('start', ''),
            event.get('end', '')))
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
    calendar = create_calendar(service, data_dict)
    events = create_events(data_dict)
    add_events(service, calendar, events)
