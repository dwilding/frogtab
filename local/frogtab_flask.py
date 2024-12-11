import sys
from os import getpid, kill
from signal import SIGINT
from json import loads
from flask import Flask, render_template, send_from_directory, request, make_response
from logging import getLogger
from frogtab_backend import backend


# Set config

args = sys.argv[1:]
if len(args) != 1:
    print('Usage: python frogtab_flask.py <json_config>')
    sys.exit(2)
config = loads(args[0])
app = Flask(__name__, static_url_path='/')


# Deinfe static routes

@app.route('/')
def serve_index():
    return render_template('index.html', server_base=config['registration_server'])

@app.route('/icon-normal')
def serve_icon_normal():
    return render_template('icon-normal.html', server_base=config['registration_server'])

@app.route('/icon-notify')
def serve_icon_notify():
    return render_template('icon-notify.html', server_base=config['registration_server'])

@app.route('/help')
def serve_help():
    return render_template('help.html', server_base=config['registration_server'])

@app.route('/<string:file>')
def serve_file(file):
    if '.' in file:
        return send_from_directory(app.static_folder, file)
    else:
        return send_from_directory(app.static_folder, f'{file}.html')


# Define service routes

@app.route('/service/get-methods')
def get_methods():
    return backend.methods()

@app.route('/service/post-data', methods=['POST'])
def post_data():
    body = request.get_json()
    return backend.save_data(body['key'], body['data'])

@app.route('/service/post-add-message', methods=['POST'])
def add_message():
    body = request.get_json()
    return backend.add_message(body['message'])

@app.route('/service/post-remove-messages', methods=['POST'])
def remove_messages():
    return backend.remove_messages()

@app.route('/service/post-stop', methods=['POST'])
def post_stop():
    kill(getpid(), SIGINT)
    return make_response('', 204)


# Start Flask

getLogger('werkzeug').disabled = True
app.run(port=config['local_port'])