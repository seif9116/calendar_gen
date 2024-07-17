from openai import OpenAI
from openai._types import FileTypes, NotGiven
from openai.types.beta.thread_create_params import MessageAttachment
from openai.types.file_object import FileObject
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.message import Message
from openai.types.beta.assistant_tool_param import AssistantToolParam
from typing import List, Any, Dict, TextIO, Iterable
from dotenv import load_dotenv
import os
import json
from io import BufferedReader

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

PROMPT: str = ('Read my attached pdf and get the events for it by using this'
         'get_events function. You only want to fill out Midterms, Final Exams,'
         ' Assignments, Quizes, and labs as events. I want you to open the file to get'
         'the information')

INPUT_FOLDER: str = 'input'

def create_client() -> OpenAI:
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    return client


def get_calendar_gen_assistant(client: OpenAI) -> Assistant:
    assistants = client.beta.assistants.list()
    for assistant in assistants:
        if assistant.name == 'Calendar File Generator':
            if assistant.tools != TOOLS:
                return client.beta.assistants.update(
                    assistant_id=assistant.id,
                    tools=TOOLS
                )
            return assistant

    return client.beta.assistants.create(
        name='Calendar File Generator',
        instructions=('Your job is to generate calendar files. You do this by'
                     'only using the get_events function'),
        temperature=0.00001, # to make results as deterministic as possible
        model='gpt-4o',
        tools=TOOLS
    )



def get_file_streams(input_folder: str = INPUT_FOLDER) -> List[FileTypes]:
    return [open(os.path.join(input_folder, file_name), 'rb')
        for file_name in os.listdir(input_folder)]

def get_events(input_file: str) -> Any:
    client: OpenAI = create_client()
    assistant: Assistant = get_calendar_gen_assistant(client)
    file_streams: List[FileTypes] = get_file_streams(INPUT_FOLDER)

    message_files: List[FileObject] = [
        client.files.create(file=file_stream, purpose='assistants')
        for file_stream in file_streams
    ]

    attachments: Iterable[MessageAttachment] | None = [
        {
            'file_id': message_file.id,
            'tools': [
                {
                    'type': 'file_search'
                }
            ]
        }
        for message_file in message_files
    ]

    thread: Thread = client.beta.threads.create(
        messages = [
            {
                'role': 'user',
                'content': PROMPT,
                'attachments': attachments
            }
        ]
    )

    run: Run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id = assistant.id
    )

    try:
        if run.required_action is None:
            raise ValueError("Required action is None")
        data_dict: Any = json.loads(run
            .required_action
            .submit_tool_outputs
            .tool_calls[0]
            .function
            .arguments)
    except (AttributeError, IndexError, KeyError, TypeError, json.JSONDecodeError) as e:
        raise ValueError("Failed to parse the required data") from e

    return data_dict
