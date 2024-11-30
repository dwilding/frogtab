from dataclasses import dataclass
from enum import Enum, auto
from requests import get, post, exceptions
from frogtab_helpers import backend


@dataclass
class FrogtabLocalConfig:
    port: int
    server: str


def _import_config():
    try:
        from config import local_port
    except ImportError:
        local_port = 5000
    try:
        from config import registration_server
    except ImportError:
        registration_server = 'https://frogtab.com/'
    return FrogtabLocalConfig(
        port=local_port,
        server=registration_server,
    )


config = _import_config()

# As a side effect, importing config sets backup methods on `backend` (via the @backup decorator)
# lib.py exposes `backend` along with its backup methods


class RequestOutcome(Enum):
    NO_CONNECTION = auto()
    UNEXPECTED_APP = auto()
    APP_FAILURE = auto()
    APP_SUCCESS = auto()


class FrogtabLocalClient():
    def __init__(self, port):
        self._port = port

    def probe(self) -> RequestOutcome:
        try:
            response = get(f'http://127.0.0.1:{self._port}/service/get-methods')
        except exceptions.ConnectionError:
            return RequestOutcome.NO_CONNECTION
        if response.status_code != 200:
            return RequestOutcome.UNEXPECTED_APP
        response_json = response.json()
        try:
            response_json = response.json()
        except exceptions.JSONDecodeError:
            return RequestOutcome.UNEXPECTED_APP
        if not isinstance(response_json, list):
            return RequestOutcome.UNEXPECTED_APP
        return RequestOutcome.APP_SUCCESS

    def add_message(self, instance_id, message) -> RequestOutcome:
        try:
            response = post(f'http://127.0.0.1:{self._port}/service/post-add-message', json={
                'instance_id': instance_id,
                'message': message
            })
        except exceptions.ConnectionError:
            return RequestOutcome.NO_CONNECTION
        if response.status_code != 200:
            return RequestOutcome.UNEXPECTED_APP
        try:
            response_json = response.json()
        except exceptions.JSONDecodeError:
            return RequestOutcome.UNEXPECTED_APP
        if not isinstance(response_json, dict) or 'success' not in response_json:
            return RequestOutcome.UNEXPECTED_APP
        if not response_json['success']:
            return RequestOutcome.APP_FAILURE
        return RequestOutcome.APP_SUCCESS