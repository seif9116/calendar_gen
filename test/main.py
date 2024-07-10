'''
TODO:
- [] Go trhouhg datacamp course and change implementation to use 
chatgpt functions
- [] Use .ics file + syllabus and integrate into google sheets
'''

from openai import OpenAI


function_descriptions = [
    {
        'name': 'Scans Syllabus',
        'description': 'Scans a syllabus and returns relevant information',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the course'
                },
                'code': {
                    'type': 'string',
                    'description': 'Course code'
                },
                'class_time': {
                    'type': 'string',
                    'description': 'Time of the classes'
                },
                'class_location': {
                    'type': 'string',
                    'description': 'Location of the classes'
                },
                'midterms': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'number': {
                                'type': 'integer',
                                'description': 'Midterm number'
                            },
                            'covering': {
                                'type': 'string',
                                'description': 'What the midterm covers'
                            },
                            'date': {
                                'type': 'string',
                                'description': 'Date of the midterm'
                            },
                            'weight': {
                                'type': 'number',
                                'description': 'Weight of the midterm in percentage'
                            }
                        }
                    }
                },
                'assignments': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': 'Title of the assignment'
                            },
                            'due_date': {
                                'type': 'string',
                                'description': 'Due date of the assignment'
                            },
                            'weight': {
                                'type': 'number',
                                'description': 'Weight of the assignment in percentage'
                            }
                        }
                    }
                },
                'quizzes': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': 'Title of the quiz'
                            },
                            'date': {
                                'type': 'string',
                                'description': 'Date of the quiz'
                            }
                        }
                    }
                },
                'quizzes_weight': {
                    'type': 'number',
                    'description': 'Cumulative weight of all quizzes in percentage'
                },
                'final': {
                    'type': 'object',
                    'properties': {
                        'date': {
                            'type': 'string',
                            'description': 'Date of the final exam'
                        },
                        'time': {
                            'type': 'string',
                            'description': 'Time of the final exam'
                        },
                        'location': {
                            'type': 'string',
                            'description': 'Location of the final exam'
                        },
                        'covering': {
                            'type': 'string',
                            'description': 'What the final exam covers'
                        },
                        'weight': {
                            'type': 'number',
                            'description': 'Weight of the final exam in percentage'
                        }
                    }
                },
                'labs': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': 'Title of the lab'
                            },
                            'due_date': {
                                'type': 'string',
                                'description': 'Due date of the lab'
                            }
                        }
                    }
                },
                'labs_weight': {
                    'type': 'number',
                    'description': 'Cumulative weight of all labs in percentage'
                }
            }
        }
    }
]


template

with open('example.txt', 'r') as file:
    example = file.read()


client = OpenAI()

assistant = client.beta.assistants.create(
    name='Calendar File Generator',
    instructions='Your job is to generate calendar files. You do this without'
                 'without providing any explanations, you only give the file'
                 'You want to make sure to include finals, midterms,'
                 'assignments, quizzes, labs, tests, etc.',
    model='gpt-4o',
    tools=[{'type': 'file_search'}]
)

# Upload the user provided file to OpenAI
message_file = client.files.create(
    file=open('syllabus.pdf', 'rb'), purpose='assistants'
)

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
    messages=[
    {
        'role': 'user',
        'content': 'Go through my syllabus and create for me a .ics file'
                   ' keep in mind that my time zone is Mountain Daylight '
                   "Saving Time and that I'm in Edmonton, Alberta, Canada"
                   'As well only give me the .ics file, do not give me anything'
                   'else, no explanations, nothing. Thank you!' + example,
        # Attach the new file to the message.
        'attachments': [
            {'file_id': message_file.id, 'tools': [{'type': 'file_search'}]}
        ],
        }
    ]
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id,
                                                  run_id=run.id))

message_content = messages[0].content[0].text
print(message_content.value)

