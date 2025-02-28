from pathlib import Path
import subprocess
import json
import time

import requests

from ._version import __version__
from ._exceptions import (
    ReadError,
    WriteError,
    WrongVersionError,
    WrongAppError,
    RunningError,
    NotRunningError
)

def get_port(config_path: Path) -> int:
    config = _read_config(config_path)
    return config["port"]

def get_expose(config_path: Path) -> bool:
    config = _read_config(config_path)
    return config["expose"]

def get_backup_file(config_path: Path) -> str:
    config = _read_config(config_path)
    return config["backupFile"]

def get_registration_server(config_path: Path) -> str:
    config = _read_config(config_path)
    return config["registrationServer"]

def set_port(config_path: Path, port: int) -> None:
    config = _read_config(config_path)
    _require_not_running(config["port"])
    config["port"] = port
    _write_json(config, config_path)

def set_expose(config_path: Path, expose: bool) -> None:
    config = _read_config(config_path)
    _require_not_running(config["port"])
    config["expose"] = expose
    _write_json(config, config_path)

def set_backup_file(config_path: Path, backup_file: str) -> None:
    config = _read_config(config_path)
    _require_not_running(config["port"])
    config["backupFile"] = backup_file
    _write_json(config, config_path)

def set_registration_server(config_path: Path, registration_server: str) -> None:
    config = _read_config(config_path)
    _require_not_running(config["port"])
    config["registrationServer"] = registration_server
    _write_json(config, config_path)

def _require_not_running(port: int) -> None:
    try:
        running = is_running(port)
    except WrongAppError:
        running = False
    except WrongVersionError:
        running = True
    if running:
        raise RunningError(port)

def _read_config(config_path: Path) -> dict:
    if not config_path.is_file():
        config = {
            "port": 5000,
            "expose": False,
            "backupFile": "Frogtab_backup.json",
            "registrationServer": "https://frogtab.com/",
            "internalState": {
                "pairingKey": "",
                "messages": []
            }
        }
        _write_json(config, config_path)
    return _read_json(config_path)

def _read_json(json_path: Path) -> dict:
    try:
        content = json_path.read_text(encoding="utf-8")
        return json.loads(content)
    except PermissionError:
        raise ReadError(json_path)

def _write_json(data: dict, json_path: Path) -> None:
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        json_path.write_text(content, encoding="utf-8")
    except PermissionError:
        raise WriteError(json_path)

def start(config_path: Path) -> bool:
    config = _read_config(config_path)
    port = config["port"]
    if is_running(port):
        return False
    # Ensure that config file and backup file are writable
    _write_json(config, config_path)
    backup_path = Path(config["backupFile"])
    if backup_path.is_file():
        data = _read_json(backup_path)
        _write_json(data, backup_path)
    else:
        _write_json({}, backup_path)
    # Run the server as a separate process
    # (raises TypeError if config_path doesn't implement __fspath__)
    subprocess.Popen(
        ["serve-frogtab", config_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    _wait_for_connection(port)
    return True

def get_running_version(port: int) -> str:
    try:
        response = requests.get(f"http://localhost:{port}/service/get-version")
    except requests.exceptions.ConnectionError:
        raise NotRunningError(port)
    if not "X-Frogtab-Local" in response.headers:
        raise WrongAppError(port)
    if response.status_code != 200:
        raise RuntimeError(f"no version (port {port})")
    return response.text

def is_running(port: int) -> bool:
    try:
        version = get_running_version(port)
    except NotRunningError:
        return False
    if version != __version__:
        raise WrongVersionError(port, version)
    return True

def stop(port: int) -> bool:
    try:
        response = requests.post(f"http://localhost:{port}/service/post-stop")
    except requests.exceptions.ConnectionError:
        return False
    if not "X-Frogtab-Local" in response.headers:
        raise WrongAppError(port)
    _wait_for_no_connection(port)
    return True

def send(port: int, task: str) -> None:
    try:
        response = requests.post(f"http://localhost:{port}/service/post-add-message", json={
            "message": task
        })
    except requests.exceptions.ConnectionError:
        raise NotRunningError(port)
    if not "X-Frogtab-Local" in response.headers:
        raise WrongAppError(port)

def _wait_for_connection(port: int) -> None:
    delay = 0.2
    for attempt in range(4):
        time.sleep(delay)
        try:
            requests.get(f"http://localhost:{port}/service/get-version")
        except requests.exceptions.ConnectionError:
            delay *= 2
            continue
        return
    raise RuntimeError(f"timeout (port {port})")

def _wait_for_no_connection(port: int) -> None:
    delay = 0.2
    for attempt in range(4):
        time.sleep(delay)
        try:
            requests.get(f"http://localhost:{port}/service/get-running-version")
        except requests.exceptions.ConnectionError:
            return
        delay *= 2
    raise RuntimeError(f"timeout (port {port})")