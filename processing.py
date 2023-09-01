import openai
import os

def get_dates(db, k: int):
    query = "What are the dates, times and locations for Midterms, Quizzes, Assignemnts, and Final Exams" 
    return db.similarity_search(query, k=k)

def process_pages(docs):
    '''This function should summarize the pages so that they only
    include important information and dates'''
    prompt = 'Summarize this page of info so that it only contains important information and dates that would be relevant in a calendar'
    pages = [openai.Completion.create(
            model='text-davinci-003',
            prompt = f'{prompt}\n {doc.page_content}')['choices'][0]['message']['content'] for doc in docs]
    print(pages)
    return pages

def create_ics_text(info):
    header = '### Create .ics files only and with no explanation \n'
    subheader = '### Use the following information to create calendar events for my Final Exams, Midterms, Quizzes, and Assignments \n'
    subsubheader = '### As well keep in mind I live in Edmonton, Alberta.'
    
    init_ics = header + subheader + subsubheader
    for page in info:
        init_ics += page.page_content
    print(init_ics)
    return openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=[
                    {'role': 'user', 'content': init_ics}
                ]
            )['choices'][0]['message']['content']

def create_ics(db, k=15):
    gen_path = os.path.join(os.path.dirname(__file__), "gen")
    ics_text = create_ics_text(get_dates(db,k))

    write_path = os.path.join(gen_path, 'syllabus.ics') 
    with open(write_path, 'w') as f:
        f.write(ics_text)

    return write_path

