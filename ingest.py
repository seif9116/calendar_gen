import os
import openai
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def ingest_data(file_path):

    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    file_path = os.path.expanduser('~/university/bachelor_3/fall/ACCTG311/syllabus.pdf')
    loader = PyPDFLoader(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100
            )
    print('loading and splitting data...')
    docs = loader.load_and_split(text_splitter)
    print('loading and splitting data completed')

    print('creating vector store...')
    db = Chroma.from_documents(documents=docs, 
                               embedding=OpenAIEmbeddings())
    return db
