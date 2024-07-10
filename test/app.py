'''
Idea: Upload syllabus -> turn into json file 
-> send json file to "backend" -> 
"backend" takes json file and compiles it into 
.ics file 
"backend" also takes json file and adds it to a 
special google sheet
'''


from typing import List, Any, Dict
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import os


template = """/
Scan the following syllabi and return the relevant details.
If the data is missing just return N/A
Syllabus: {syllabus}
"""


def create_page() -> None:
    st.write('# Syllabus Calendar Generator')
    st.write('### Upload your Syllabus')


def main() -> None:
    tools: List[Dict[str, Any]] = [
        {'type': 'file_search'},
        {'type': 'function',
            'function': {
                'name': 'scan_syllabus',
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
                    },
                    'required': ['name', 'code'],
                },
            }
        },
    ]
    create_page()

    status = st.empty()
    details = st.empty()
    file: None = st.file_uploader("PDF, Word Doc", type=["pdf, docx"])

    load_dotenv()
    client: OpenAI = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    # TODO: Edit this to use the function
    assistant = client.beta.assistants.create(
            name='Calendar File Generator',
            instructions='Your job is to generate calendar files. You do this without'
            'without providing any explanations, you only give the file'
            'You want to make sure to include finals, midterms,'
            'assignments, quizzes, labs, tests, etc. Use the function tool',
            model='gpt-4o',
            tools=tools,
            #tool_choice=[{'type': 'function', 'function': {'name': 'scan_syllabus'}}],
            response_format={'type': 'json_object'}
            )
    if file is not None:
        with st.spinner('Scanner...'):
            message_file = client.files.create(
                file=file, purpose='assistants'
            )

            prompt = ''



if __name__ == '__main__':
    main()
