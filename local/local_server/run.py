import sys
import os
import signal
import logging
import flask

from helpers import Config, backend


# Load config

args = sys.argv[1:]
if len(args) != 1:
    sys.exit(2)
config = Config(args[0])
app = flask.Flask(__name__, static_url_path='/')


# Deinfe static routes

@app.route('/')
def serve_index():
    return flask.render_template('index.html', server_base=config.registration_server)

@app.route('/icon-normal')
def serve_icon_normal():
    return flask.render_template('icon-normal.html', server_base=config.registration_server)

@app.route('/icon-notify')
def serve_icon_notify():
    return flask.render_template('icon-notify.html', server_base=config.registration_server)

@app.route('/help')
def serve_help():
    return flask.render_template('help.html', server_base=config.registration_server)

@app.route('/<string:file>')
def serve_file(file):
    if '.' in file:
        return flask.send_from_directory(app.static_folder, file)
    else:
        return flask.send_from_directory(app.static_folder, f'{file}.html')


# Define service routes

@app.route('/service/get-status')
def get_status():
    return 'Frogtab Local is running'

@app.route('/service/get-methods')
def get_methods():
    return backend.methods()

@app.route('/service/post-data', methods=['POST'])
def post_data():
    body = flask.request.get_json()
    return backend.save_data(body['key'], body['data'])

@app.route('/service/post-add-message', methods=['POST'])
def add_message():
    body = flask.request.get_json()
    return backend.add_message(body['message'])

@app.route('/service/post-remove-messages', methods=['POST'])
def remove_messages():
    return backend.remove_messages()

@app.route('/service/post-stop', methods=['POST'])
def post_stop():
    os.kill(os.getpid(), signal.SIGINT)
    return flask.make_response('', 204)


# Start Flask

logging.getLogger('werkzeug').disabled = True
app.run(port=config.port)