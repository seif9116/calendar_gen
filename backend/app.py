from flask import Flask, Blueprint, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from processing import create_ics
from ingest import ingest_data
from werkzeug.utils import secure_filename
from __init__ import PORT, FLASK_ENV

import os
import openai

def handle_upload(pdf_path):
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

    @app_bp.route("/help")
    def help():
        return "Request received"

    @app_bp.route("/")
    def serve():
        print("serve root")

        prod_static_dir = '/calendar-gen/backend/build'
        dev_static_dir = '../app/build'
        
        static_dir = dev_static_dir if FLASK_ENV == 'DEV' else prod_static_dir
        static_file = "index.html"
        
        if os.path.exists(os.path.join(static_dir, static_file)):
            return send_from_directory(static_dir, static_file)
 
        else:
            return "index.html not found"
        
    app.register_blueprint(app_bp)

def create_app():

    app = Flask(__name__)

    CORS(app)

    print(FLASK_ENV, PORT)

    if FLASK_ENV == 'PROD': 
        app.static_folder = '/calendar-gen/backend/build/static' 
        register_routes(app) 
        return app
    else:
        app.static_folder = '../app/build/static'
        register_routes(app) 
        app.run(debug=True, host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    create_app()