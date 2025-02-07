from pathlib import Path
from typing import Callable, Any, Optional

import json
import subprocess
import requests
import time

from .version import __version__


class Controller():
    def __init__(
        self,
        config_file: str,
        on_read_error: Optional[Callable[[str], Any]] = None,
        on_write_error: Optional[Callable[[str], Any]] = None
    ):
        self.config_file = config_file
        self.on_read_error = on_read_error
        self.on_write_error = on_write_error
        if Path(config_file).is_file():
            self._config = self._read_json(config_file)
        else:
            self._config = {
                'port': 5000,
                'backupFile': 'Frogtab_backup.json',
                'registrationServer': 'https://frogtab.com/',
                'internalState': {
                    'pairingKey': '',
                    'messages': []
                }
            }
            self._write_json(self._config, config_file)

    def is_running(self) -> bool:
        try:
            response = requests.get(f'http://localhost:{self.port}/service/get-running')
        except requests.exceptions.ConnectionError:
            return False
        if not 'X-Frogtab-Local' in response.headers:
            raise WrongAppError
        if response.headers['X-Frogtab-Local'] != __version__:
            raise WrongVersionError
        return True

    def start(self) -> bool:
        if self.is_running():
            return False
        # Ensure that config file is writeable
        self._config = self._read_json(self.config_file)
        self._write_json(self._config, self.config_file)
        # Ensure that backup file is writeable
        if Path(self.backup_file).is_file():
            data = self._read_json(self.backup_file)
            self._write_json(data, self.backup_file)
        else:
            self._write_json({}, self.backup_file)
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
        self._config = self._read_json(self.config_file)
        self._config['port'] = port
        self._write_json(self._config, self.config_file)

    def set_backup_file(self, backup_file: str) -> None:
        self._require_not_running()
        self._config = self._read_json(self.config_file)
        self._config['backupFile'] = backup_file
        self._write_json(self._config, self.config_file)

    def set_registration_server(self, registration_server: str) -> None:
        self._require_not_running()
        self._config = self._read_json(self.config_file)
        self._config['registrationServer'] = registration_server
        self._write_json(self._config, self.config_file)

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
        except WrongVersionError:
            running = True
        if running:
            raise RunningError

    def _read_json(self, json_file: str) -> dict:
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except PermissionError:
            if self.on_read_error:
                self.on_read_error(json_file) # Expect this to call sys.exit()
            raise

    def _write_json(self, data: dict, json_file: str) -> None:
        try:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except PermissionError:
            if self.on_write_error:
                self.on_write_error(json_file) # Expect this to call sys.exit()
            raise


class WrongAppError(Exception):
    pass

class WrongVersionError(Exception):
    pass

class NotRunningError(Exception):
    pass

class RunningError(Exception):
    pass