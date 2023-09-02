from flask import Flask, Blueprint, request, jsonify, send_file
from flask_cors import CORS
from processing import create_ics
from dotenv import load_dotenv
from ingest import ingest_data
import os
import openai
from werkzeug.utils import secure_filename

def handle_upload(pdf_path):
    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    db = ingest_data(pdf_path)
    ics_path = create_ics(db)
    return ics_path

def register_routes(app: Flask):

    app_bp = Blueprint("app_bp", __name__)

    @app_bp.route("/api/syllabus", methods=["POST"])
    def handle_syllabus():
        if 'syllabus' in request.files:
            file = request.files['syllabus']
            print(file)
            
            filename = secure_filename(file.filename)
            file_path = os.path.join("uploaded_files", filename)
            file.save(file_path)

            ics_path = handle_upload(file_path) 
            return send_file(
                ics_path, 
                as_attachment=True, 
                download_name='syllabus.ics'
            )

        return jsonify("error") 

    @app_bp.route("/")
    def index():
        return "Hello, World"
    
    app.register_blueprint(app_bp)


def create_app(dev=True):

    app = Flask(__name__)
    CORS(app)
    register_routes(app)

    if dev: 
        app.run(debug=True)
    else:   
        return app