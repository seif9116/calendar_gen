import openai

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
    init_ics = "Use the following information to create .ics for my Final Exams, Midterms, Quizzes, Assignments \n As well keep in mind, I live in Edmonton Alberta"
    for page in info:
        init_ics += page
    print(init_ics)
    return openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=[
                    {'role': 'user', 'content': init_ics}
                ]
            )['choices'][0]['message']['content']

def create_ics(db, k=6):
    ics_text = create_ics_text(process_pages(get_dates(db, k)))
    with open('syllabus.ics', 'w') as f:
        f.write(ics_text)

