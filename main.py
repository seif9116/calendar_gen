import os
from processing import create_ics
import openai
from dotenv import load_dotenv
from ingest import ingest_data

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

def main():
    db = ingest_data('')
    create_ics(db)

if __name__ == '__main__':
    main()
