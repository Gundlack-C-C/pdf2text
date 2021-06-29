from flask import json, jsonify, Flask, render_template, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS

import logging
import argparse
import os, sys
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from PDFReader import pdf2text

UPLOAD_FOLDER = './.upload/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
app.add_url_rule("/info/<name>", endpoint="info_file", build_only=True)
app.add_url_rule("/upload", endpoint="upload", build_only=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def try_save_file_input(files):
    if 'file' not in files:
        flash('No file part')
        raise BadRequest("Missing input! - not found in request.files")
    
    file = files['file']

    if file.filename == '':
        flash('No selected file')
        raise BadRequest("Invalid Input - no selected file - filename is empty")

    if not allowed_file(file.filename):
        flash('Format not supported')
        raise BadRequest(f"Invalid Input - format is not supported - supported only: {ALLOWED_EXTENSIONS}")

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('upload'))



@app.route('/api/text', methods=['POST'])
def text_extraction():
    filename = try_save_file_input(request.files)
    text = pdf2text(f"{app.config['UPLOAD_FOLDER']}{filename}")
    return jsonify({'text': text, 'id': filename, 'url': url_for('info_file', name=filename)})


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        filename = try_save_file_input(request.files)
        return redirect(url_for('info_file', name=filename))
    
    return render_template('file_upload.html')

@app.route('/info/<name>')
def info_file(name):
    text = pdf2text(f"{app.config['UPLOAD_FOLDER']}{name}")
    return render_template('file_upload_info.html', filename=name, text=text)

@app.route('/download/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__':

    try:
        LOG = "./.log/PDF_KEYWORD_SERVER.log"

        # Setup Argument Parser
        parser = argparse.ArgumentParser(description='Argument Parser')
        parser.add_argument('-l', '--log', dest='LOGFILE', type=str, default=LOG,
                            help=f'path for logfile (default: {LOG})')
        parser.add_argument("--production", action='store_const', help="set to production mode", const=True, default=False)

        args = parser.parse_args()
        # Check if production is set
        PRODUCTION = args.production
        os.environ['PRODUCTION'] = str(PRODUCTION)

        if not os.path.exists(os.path.abspath(os.path.dirname(args.LOGFILE))):
                os.makedirs(os.path.abspath(os.path.dirname(args.LOGFILE)))

        if not os.path.exists(os.path.abspath(os.path.dirname(UPLOAD_FOLDER))):
                os.makedirs(os.path.abspath(os.path.dirname(UPLOAD_FOLDER)))
        
        # Setup Logging
        logging.basicConfig(filename=args.LOGFILE, level=logging.INFO if PRODUCTION else logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        logging.info(f"Starting Server with [{args}]")
    
        # Start Server
        app.run(host="0.0.0.0", debug=False, port = 5001)

    except Exception as e:
        logging.error(e)
