from typing import Any, List
import os.path
import google.oauth2.credentials
import google.auth.external_account_authorized_user
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai._types import FileTypes, NotGiven
from typing import Iterable


# If modifying these scopes, delete the file token.json.
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
SHEET_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

TOOLS: Iterable[AssistantToolParam] | NotGiven = [
    {
        'type': 'file_search'
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_events',
            'description': 'Gets events from a syllabus',
            'parameters': {
                'type': 'object',
                'properties': {
                    'course name': {
                        'type': 'string',
                        'description': 'name of the course'
                    },
                    'course code': {
                        'type': 'string',
                        'description': 'code of the course'
                    },
                    'events': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'description': 'Each calendar event',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'name of event',
                                },
                                'start': {
                                    'type': 'string',
                                    'description': ('start date, format: YYYY-MM-DD HH:MM:SS. '
                                                   'For all-day events, use YYYY-MM-DD. This is required. '
                                                   'Exclude events without a start date or with unclear dates '
                                                   'such as "see eclass for dates". For midterms, finals, quizzes, etc., '
                                                   'if not asynchronous, use the class start time. Do not leave this empty.')
                                },
                                'end': {
                                    'type': 'string',
                                    'description': ('end date, format should be '
                                                   'YYYY-MM-DD HH:MM:SS. If it is an all-day '
                                                   'event/reminder, use YYYY-MM-DD without time. '
                                                   'For midterms, finals, quizzes, etc., if not asynchronous use the class end time.')
                                },
                                'description': {
                                    'type': 'string',
                                    'description': 'description of the event'
                                },
                                'location': {
                                    'type': 'string',
                                    'description': 'location of the event'
                                },
                                'EventType': {
                                    'type': 'string',
                                    'description': 'type of event',
                                    'enum': [
                                        'Assignment',
                                             'Quiz',
                                             'Midterm',
                                             'Final',
                                             'Lab',
                                             'Other'
                                    ],
                                },
                                'weight': {
                                    'type': 'object',
                                    'description': 'weight of the event',
                                    'properties': {
                                        'value': {
                                            'type': 'number',
                                            'description': ('value of the weight. For example 10 for 10%. '
                                                'If special grading scheme for example drop lowest assignment, just average'
                                                ' the weights of all assignments.')
                                        },
                                        'note': {
                                            'type': 'string',
                                            'description': 'note about the weight. For example "drop lowest grade"'
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'required': ['course name','course code', 'events']
            },

        }
    }
]
Creds = (google.oauth2.credentials.Credentials
        | google.auth.external_account_authorized_user.Credentials
        | None)


def get_service(api_name: str,
    api_version: str,
    scopes: List[str],
    token_file: str,
    port: int) -> Any:
    creds: Creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=port)
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    try:
        service = build(api_name, api_version, credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
