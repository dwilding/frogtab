from pathlib import Path
import json
import time

import requests

from .version import __version__
from . import exceptions

def get_port(config_file: Path) -> int:
    config = _read_config(config_file)
    return config["port"]

def get_backup_file(config_file: Path) -> str:
    config = _read_config(config_file)
    return config["backupFile"]

def get_registration_server(config_file: Path) -> str:
    config = _read_config(config_file)
    return config["registrationServer"]

def set_port(config_file: Path, port: int) -> None:
    config = _read_config(config_file)
    _require_not_running(config["port"])
    config["port"] = port
    _write_json(config, config_file)

def set_backup_file(config_file: Path, backup_file: str) -> None:
    config = _read_config(config_file)
    _require_not_running(config["port"])
    config["backupFile"] = backup_file
    _write_json(config, config_file)

def set_registration_server(config_file: Path, registration_server: str) -> None:
    config = _read_config(config_file)
    _require_not_running(config["port"])
    config["registrationServer"] = registration_server
    _write_json(config, config_file)

def _require_not_running(port: int) -> None:
    try:
        running = is_running(port)
    except exceptions.WrongApp:
        running = False
    except exceptions.WrongVersion:
        running = True
    if running:
        raise exceptions.Running(port)

def _read_config(config_file: Path) -> dict:
    if not config_file.is_file():
        config = {
            "port": 5000,
            "backupFile": "Frogtab_backup.json",
            "registrationServer": "https://frogtab.com/",
            "internalState": {
                "pairingKey": "",
                "messages": []
            }
        }
        _write_json(config, config_file)
    return _read_json(config_file)

def _read_json(json_file: Path) -> dict:
    try:
        content = json_file.read_text(encoding="utf-8")
        return json.loads(content)
    except PermissionError:
        raise exceptions.Read(json_file)

def _write_json(data: dict, json_file: Path) -> None:
    try:
        content = json.dumps(data, indent=2, ensure_ascii=False)
        json_file.write_text(content, encoding="utf-8")
    except PermissionError:
        raise exceptions.Write(json_file)

def get_running_version(port: int) -> str:
    try:
        response = requests.get(f"http://localhost:{port}/service/get-version")
    except requests.exceptions.ConnectionError:
        raise exceptions.NotRunning(port)
    if not "X-Frogtab-Local" in response.headers:
        raise exceptions.WrongApp(port)
    return response.text

def is_running(port: int) -> bool:
    try:
        version = get_running_version(port)
    except exceptions.NotRunning:
        return False
    if version != __version__:
        raise exceptions.WrongVersion(port, version)
    return True

def stop(port: int) -> bool:
    try:
        response = requests.post(f"http://localhost:{port}/service/post-stop")
    except requests.exceptions.ConnectionError:
        return False
    if not "X-Frogtab-Local" in response.headers:
        raise exceptions.WrongApp(port)
    _wait_for_no_connection(port)
    return True

def send(port: int, task: str) -> None:
    try:
        response = requests.post(f"http://localhost:{port}/service/post-add-message", json={
            "message": task
        })
    except requests.exceptions.ConnectionError:
        raise exceptions.NotRunning(port)
    if not "X-Frogtab-Local" in response.headers:
        raise exceptions.WrongApp(port)

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