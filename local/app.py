from flask import Flask, send_from_directory, request
from frogtab_helpers import list_methods, save_data
from config import local_port

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

@app.route('/save/get-methods')
def get_methods():
    return list_methods()

@app.route('/save/post-data', methods=['POST'])
def post_data():
    body = request.get_json()
    key = body['key']
    return save_data(key, body['data'])

if __name__ == '__main__':
    app.run(port=local_port)