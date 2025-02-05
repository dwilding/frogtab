# TODO: Catch file I/O errors and raise more descriptive errors
#       Shall we have dedicated class methods for _read_backup_file, _read_config_file, etc
#       Then within those methods, we can catch any errors and re-raise?

from pathlib import Path

import json
import subprocess
import requests
import time


class Controller():
    def __init__(self, config_file: str):
        self.config_file = config_file
        if Path(config_file).is_file():
            self._config = _read_json(config_file)
        else:
            self._config = {
                'port': 5000,
                'backupFile': 'Frogtab_backup.json',
                'registrationServer': 'https://frogtab.com/',
                'internalState': {
                    'pairingKey': '',
                    'messages': ''
                }
            }
            _write_json(self._config, config_file)

    def is_running(self) -> bool:
        try:
            response = requests.get(f'http://localhost:{self.port}/service/get-running')
        except requests.exceptions.ConnectionError:
            return False
        if not 'X-Frogtab-Local' in response.headers:
            raise WrongAppError
        if response.status_code != 204:
            raise RuntimeError(f'unexpected response (port {self.port})')
        return True

    def start(self) -> bool:
        if self.is_running():
            return False
        # Ensure that config file is writeable
        self._config = _read_json(self.config_file)
        _write_json(self._config, self.config_file)
        # Ensure that backup file is writeable
        if Path(self.backup_file).is_file():
            data = _read_json(self.backup_file)
            _write_json(data, self.backup_file)
        else:
            _write_json({}, self.backup_file)
        # Run the server
        subprocess.Popen([
            'python',
            Path(__file__).parent / 'local_server' / 'server.py',
            self.config_file
        ], stdout=subprocess.DEVNULL)
        self._wait_for_connection()
        return True

    def stop(self) -> bool:
        try:
            response = requests.post(f'http://localhost:{self.port}/service/post-stop')
        except requests.exceptions.ConnectionError:
            return False
        if not 'X-Frogtab-Local' in response.headers:
            raise WrongAppError
        if response.status_code != 204:
            raise RuntimeError(f'unexpected response (port {self.port})')
        self._wait_for_no_connection()
        return True

    def send(self, task: str) -> None:
        try:
            response = requests.post(f'http://localhost:{self.port}/service/post-add-message', json={
                'message': task
            })
        except requests.exceptions.ConnectionError:
            raise NotRunningError
        if not 'X-Frogtab-Local' in response.headers:
            raise WrongAppError
        if response.status_code != 204:
            raise RuntimeError(f'unexpected response (port {self.port})')

    @property
    def port(self) -> int:
        return self._config['port']

    @property
    def backup_file(self) -> str:
        return self._config['backupFile']

    @property
    def registration_server(self) -> str:
        return self._config['registrationServer']

    def set_port(self, port: int) -> None:
        self._require_not_running()
        self._config = _read_json(self.config_file)
        self._config['port'] = port
        _write_json(self._config, self.config_file)

    def set_backup_file(self, backup_file: str) -> None:
        self._require_not_running()
        self._config = _read_json(self.config_file)
        self._config['backupFile'] = backup_file
        _write_json(self._config, self.config_file)

    def set_registration_server(self, registration_server: str) -> None:
        self._require_not_running()
        self._config = _read_json(self.config_file)
        self._config['registrationServer'] = registration_server
        _write_json(self._config, self.config_file)

    def _wait_for_connection(self) -> None:
        delay = 0.2
        for attempt in range(4):
            time.sleep(delay)
            try:
                requests.get(f'http://localhost:{self.port}/service/get-running')
            except requests.exceptions.ConnectionError:
                delay *= 2
                continue
            return
        raise RuntimeError(f'timeout (port {self.port})')

    def _wait_for_no_connection(self) -> None:
        delay = 0.2
        for attempt in range(4):
            time.sleep(delay)
            try:
                requests.get(f'http://localhost:{self.port}/service/get-running')
            except requests.exceptions.ConnectionError:
                return
            delay *= 2
        raise RuntimeError(f'timeout (port {self.port})')

    def _require_not_running(self) -> None:
        try:
            running = self.is_running()
        except WrongAppError:
            running = False
        if running:
            raise RunningError


class WrongAppError(Exception):
    pass

class NotRunningError(Exception):
    pass

class RunningError(Exception):
    pass

def _read_json(json_file: str) -> dict:
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def _write_json(data: dict, json_file: str) -> None:
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)