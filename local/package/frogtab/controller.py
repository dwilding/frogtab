from pathlib import Path
from typing import Callable, Any, Optional

import json
import subprocess

from .client import NotRunningError, WrongAppError, WrongVersionError, Client

class RunningError(Exception):
    pass


class Controller(Client):
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
                self.on_read_error(json_file) # expect this to call sys.exit()
            raise

    def _write_json(self, data: dict, json_file: str) -> None:
        try:
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except PermissionError:
            if self.on_write_error:
                self.on_write_error(json_file) # expect this to call sys.exit()
            raise