from flask import Flask, render_template, send_from_directory, request, make_response
from frogtab_helpers import list_methods, save_data, add_message_for, remove_messages_for
from os import getpid, kill
from signal import SIGINT

try:
    from config import local_port
except ImportError:
    local_port = 5000

try:
    from config import registration_server
except ImportError:
    registration_server = 'https://frogtab.com/'

app = Flask(__name__, static_url_path='/')

@app.route('/')
def serve_index():
    return render_template('index.html', server_base=registration_server)

@app.route('/icon-normal')
def serve_icon_normal():
    return render_template('icon-normal.html', server_base=registration_server)

@app.route('/icon-notify')
def serve_icon_notify():
    return render_template('icon-notify.html', server_base=registration_server)

@app.route('/help')
def serve_help():
    return render_template('help.html', server_base=registration_server)

@app.route('/<string:file>')
def serve_file(file):
    if '.' in file:
        return send_from_directory(app.static_folder, file)
    else:
        return send_from_directory(app.static_folder, f'{file}.html')

@app.route('/service/get-methods')
def get_methods():
    return list_methods()

@app.route('/service/post-data', methods=['POST'])
def post_data():
    body = request.get_json()
    return save_data(body['key'], body['data'])

@app.route('/service/post-add-message', methods=['POST'])
def add_message():
    body = request.get_json()
    return add_message_for(body['instance_id'], body['message'])

@app.route('/service/post-remove-messages', methods=['POST'])
def remove_messages():
    body = request.get_json()    
    return remove_messages_for(body['instance_id'])

@app.route('/service/post-stop', methods=['POST'])
def post_stop():
    kill(getpid(), SIGINT)
    return make_response('', 204)

if __name__ == '__main__':
    app.run(port=local_port)