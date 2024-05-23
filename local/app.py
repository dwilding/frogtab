from flask import Flask, send_from_directory

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