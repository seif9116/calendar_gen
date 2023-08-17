import os
import openai
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAi API Key:')
llm = OpenAI()

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
docs = db.similarity_search(query, 3)
for doc in docs:
    print(doc.page_content)

def create_ics(docs):
    init_ics = "use the following information to create .ics for my Midterms, Quizzes, Final Exams, Assignments, and Classes"
    for doc in docs:
        init_ics += doc.page_content
    return llm(init_ics)

print(create_ics(docs))
