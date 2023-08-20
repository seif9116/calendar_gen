import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from processing import create_ics
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

def main():
    db = Chroma(persist_directory='data/', embedding_function=OpenAIEmbeddings())
    create_ics(db)

if __name__ == '__main__':
    main()
