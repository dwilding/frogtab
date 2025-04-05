from pathlib import Path
import sys
import os
import signal
import json
import logging

import flask

VERSION = "2.0.0b23"

def read_json(json_path: Path) -> dict:
    content = json_path.read_text(encoding="utf-8")
    return json.loads(content)

def write_json(data: dict, json_path: Path) -> None:
    content = json.dumps(data, indent=2, ensure_ascii=False)
    json_path.write_text(content, encoding="utf-8")


# Load settings and internal state

args = sys.argv[1:]
if len(args) != 1:
    sys.exit(2)
config_path = Path(args[0])
config = read_json(config_path)


# Create a Flask app

app = flask.Flask(__name__, static_url_path="/")


# Deinfe static routes

@app.route("/")
def serve_index():
    return flask.render_template("index.html", server_base=config["registrationServer"])

@app.route("/icon-normal")
def serve_icon_normal():
    return flask.render_template("icon-normal.html", server_base=config["registrationServer"])

@app.route("/icon-notify")
def serve_icon_notify():
    return flask.render_template("icon-notify.html", server_base=config["registrationServer"])

@app.route("/help")
def serve_help():
    return flask.render_template("help.html", server_base=config["registrationServer"])

@app.route("/<string:file>")
def serve_file(file):
    if "." in file:
        return flask.send_from_directory(app.static_folder, file)
    else:
        return flask.send_from_directory(app.static_folder, f"{file}.html")


# Define service routes for the web app

@app.route("/service/post-pair", methods=["POST"])
def post_pair():
    body = flask.request.get_json()
    if body["force"] or not config["internalState"]["pairingKey"]:
        config["internalState"]["pairingKey"] = body["key"]
        write_json(config, config_path)
    elif body["key"] != config["internalState"]["pairingKey"]:
        return {
            "success": False
        }
    return {
        "success": True
    }

@app.route("/service/post-data", methods=["POST"])
def post_data():
    body = flask.request.get_json()
    if not config["internalState"]["pairingKey"]:
        config["internalState"]["pairingKey"] = body["key"]
        write_json(config, config_path)
    elif body["key"] != config["internalState"]["pairingKey"]:
        return {
            "success": False
        }
    write_json(body["data"], Path(config["backupFile"]))
    return {
        "success": True
    }

@app.route("/service/post-remove-messages", methods=["POST"])
def remove_messages():
    body = flask.request.get_json()
    if not config["internalState"]["pairingKey"]:
        config["internalState"]["pairingKey"] = body["key"]
        write_json(config, config_path)
    elif body["key"] != config["internalState"]["pairingKey"]:
        return {
            "success": False
        }
    messages = config["internalState"]["messages"]
    config["internalState"]["messages"] = []
    write_json(config, config_path)
    return {
        "success": True,
        "messages": messages
    }


# Define service routes for clients

@app.route("/service/get-version")
def get_version():
    return VERSION

@app.route("/service/post-add-message", methods=["POST"])
def add_message():
    body = flask.request.get_json()
    config["internalState"]["messages"].append(body["message"])
    write_json(config, config_path)
    return flask.make_response("", 204)

@app.route("/service/post-stop", methods=["POST"])
def post_stop():
    os.kill(os.getpid(), signal.SIGINT)
    return flask.make_response("", 204)


# Add a custom response header to identify Frogtab Local

@app.after_request
def add_custom_header(response):
    response.headers["X-Frogtab-Local"] = VERSION
    return response


# Define the entrypoint

def main():
    host = "localhost"
    if config["expose"]:
        host = "0.0.0.0"
    logging.getLogger("werkzeug").disabled = True
    app.run(
        host=host,
        port=config["port"]
    )

if __name__ == "__main__":
    main()