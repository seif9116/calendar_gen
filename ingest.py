import os
import openai
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAi API Key:')
openai.api_key = os.environ['OPENAI_API_KEY']
file_path = os.path.expanduser('~/university/bachelor_3/fall/FIN301/syllabus.pdf')
loader = PyPDFLoader(file_path)
text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100
        )
print('loading and splitting data...')
docs = loader.load_and_split(text_splitter)
print('loading and splitting data completed')

print('creating vector store...')
db = Chroma.from_documents(docs, OpenAIEmbeddings())

query = "What are the dates, times and locations for 1) Midterms, Quizzes, Final Exams, 2) Assignments, 3) Classes"
docs = db.similarity_search(query, k=6)

def create_ics(docs):
    init_ics = "use the following information to create .ics for my 1) Midterms, Quizzes, Final Exams 2) Assignments, and 3) Classes \n"
    for doc in docs:
        init_ics += doc.page_content
    print(init_ics)
    return openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                    {'role': 'user', 'content': init_ics}
                ]
            )

print(create_ics(docs)['choices'][0]['message']['content'])
