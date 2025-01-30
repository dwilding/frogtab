import requests
import time

class NotRunningError(Exception):
    pass

class UnknownAppError(Exception):
    pass

def get_running(port: int) -> bool:
    try:
        response = requests.get(f'http://localhost:{port}/service/get-running')
    except requests.exceptions.ConnectionError:
        return False
    if response.status_code != 204:
        raise UnknownAppError
    return True

def wait_for_running(port: int):
    delay = 0.2
    for attempt in range(4):
        time.sleep(delay)
        if get_running(port):
            return
        delay *= 2
    raise RuntimeError(f'timeout (port {port})')

def wait_for_not_running(port: int):
    delay = 0.2
    for attempt in range(4):
        time.sleep(delay)
        if not get_running(port):
            return
        delay *= 2
    raise RuntimeError(f'timeout (port {port})')

def post_stop(port: int) -> bool:
    try:
        response = requests.post(f'http://localhost:{port}/service/post-stop')
    except requests.exceptions.ConnectionError:
        return False
    if response.status_code != 204:
        raise UnknownAppError
    return True

def post_add_message(port: int, message: str):
    try:
        response = requests.post(f'http://localhost:{port}/service/post-add-message', json={
            'message': message
        })
    except requests.exceptions.ConnectionError:
        raise NotRunningError
    if response.status_code != 204:
        raise UnknownAppError