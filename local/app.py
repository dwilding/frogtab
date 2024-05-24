from flask import Flask, send_from_directory, request
from backend import list_services, call_service
import services

app = Flask(__name__, static_url_path='/')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<string:file>')
def serve_file(file):
    if '.' in file:
        return send_from_directory(app.static_folder, file)
    else:
        return send_from_directory(app.static_folder, f'{file}.html')

@app.route('/services/get-services')
def get_services():
    return list_services()

@app.route('/services/post-service', methods=['POST'])
def post_service():
    body = request.get_json()
    key = body['key']
    call_service(key, body['data'])
    return f'Called {key}'