import os
from dotenv import load_dotenv

load_dotenv()

FLASK_ENV = os.environ.get('FLASK_ENV')
PORT = os.environ.get('PORT', 5000)