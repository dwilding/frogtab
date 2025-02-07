import sys
import os
import signal
import json
import logging
import flask

def read_json(json_file: str) -> dict:
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(data: dict, json_file: str) -> None:
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Load config (including internal state)

args = sys.argv[1:]
if len(args) != 1:
    sys.exit(2)
config_file = args[0]
config = read_json(config_file)


# Create a Flask app

app = flask.Flask(__name__, static_url_path='/')


# Deinfe static routes

@app.route('/')
def serve_index():
    return flask.render_template('index.html', server_base=config['registrationServer'])

@app.route('/icon-normal')
def serve_icon_normal():
    return flask.render_template('icon-normal.html', server_base=config['registrationServer'])

@app.route('/icon-notify')
def serve_icon_notify():
    return flask.render_template('icon-notify.html', server_base=config['registrationServer'])

@app.route('/help')
def serve_help():
    return flask.render_template('help.html', server_base=config['registrationServer'])

@app.route('/<string:file>')
def serve_file(file):
    if '.' in file:
        return flask.send_from_directory(app.static_folder, file)
    else:
        return flask.send_from_directory(app.static_folder, f'{file}.html')


# Define service routes for the web app

@app.route('/service/post-pair', methods=['POST'])
def post_pair():
    body = flask.request.get_json()
    if body['force'] or not config['internalState']['pairingKey']:
        config['internalState']['pairingKey'] = body['key']
        write_json(config, config_file)
    elif body['key'] != config['internalState']['pairingKey']:
        return {
            'success': False
        }
    return {
        'success': True
    }

@app.route('/service/post-data', methods=['POST'])
def post_data():
    body = flask.request.get_json()
    if not config['internalState']['pairingKey']:
        config['internalState']['pairingKey'] = body['key']
        write_json(config, config_file)
    elif body['key'] != config['internalState']['pairingKey']:
        return {
            'success': False
        }
    write_json(body['data'], config['backupFile'])
    return {
        'success': True
    }

@app.route('/service/post-remove-messages', methods=['POST'])
def remove_messages():
    body = flask.request.get_json()
    if not config['internalState']['pairingKey']:
        config['internalState']['pairingKey'] = body['key']
        write_json(config, config_file)
    elif body['key'] != config['internalState']['pairingKey']:
        return {
            'success': False
        }
    messages = config['internalState']['messages']
    config['internalState']['messages'] = []
    write_json(config, config_file)
    return {
        'success': True,
        'messages': messages
    }


# Define service routes for the controller

@app.route('/service/get-running')
def get_running():
    return flask.make_response('', 204)

@app.route('/service/post-add-message', methods=['POST'])
def add_message():
    body = flask.request.get_json()
    config['internalState']['messages'].insert(0, body['message'])
    write_json(config, config_file)
    return flask.make_response('', 204)

@app.route('/service/post-stop', methods=['POST'])
def post_stop():
    os.kill(os.getpid(), signal.SIGINT)
    return flask.make_response('', 204)


# Add a custom response header to identify Frogtab Local

@app.after_request
def add_custom_header(response):
    response.headers['X-Frogtab-Local'] = '2.0.0b1'
    return response


# Run Flask

logging.getLogger('werkzeug').disabled = True
app.run(port=config['port'])