from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_voice():
    if 'voice' not in request.files:
        print("No file part")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['voice']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        file_url = f"http://127.0.0.1:5000/uploads/{filename}"
        return jsonify({'message': 'File uploaded successfully', 'file_url': file_url}), 200

    return jsonify({'error': 'Invalid file type'}), 400

# Endpoint để serve file
# @app.route('/uploads/<filename>')
# def serve_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    filename = data['filename']
    return jsonify({'text': f'/uploads/{filename}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
