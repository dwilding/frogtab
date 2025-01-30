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


# Create a Flask app

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
    backend.add_message(body['message'])
    return flask.make_response('', 204)

@app.route('/service/post-remove-messages', methods=['POST'])
def remove_messages():
    return backend.remove_messages()

@app.route('/service/post-stop', methods=['POST'])
def post_stop():
    os.kill(os.getpid(), signal.SIGINT)
    return flask.make_response('', 204)

@app.route('/service/get-running')
def get_running():
    return flask.make_response('', 204)


# Add a custom response header to identify Frogtab Local

@app.after_request
def add_custom_header(response):
    response.headers['X-Frogtab-Local'] = 1 # Value is not significant
    return response


# Run Flask

logging.getLogger('werkzeug').disabled = True
app.run(port=config.port)