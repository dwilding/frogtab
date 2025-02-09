import requests
import time

from .version import __version__

class NotRunningError(Exception):
    pass

class WrongAppError(Exception):
    pass

class WrongVersionError(Exception):
    def __init__(self, message: str, running_version: str):
        super().__init__(message)
        self.running_version = running_version


class Client():
    def __init__(self, port: int):
        self._config = {
            'port': port
        }

    @property
    def port(self) -> int:
        return self._config['port']

    def is_running(self) -> bool:
        try:
            response = requests.get(f'http://localhost:{self.port}/service/get-running')
        except requests.exceptions.ConnectionError:
            return False
        if not 'X-Frogtab-Local' in response.headers:
            raise WrongAppError
        version = response.headers['X-Frogtab-Local']
        if version != __version__:
            raise WrongVersionError(
                message=f'running version \'{version}\' does not match client version \'{__version__}\'',
                running_version=version
            )
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