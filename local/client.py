import requests
import time

class NotRunningError(Exception):
    pass

class UnknownAppError(Exception):
    pass

def get_status_with_retry(port: int, want_running: bool) -> bool:
    delay = 0.2
    for attempt in range(4):
        time.sleep(delay)
        running = get_status(port)
        if running == want_running:
            return running
        delay *= 2
    return running

def get_status(port: int) -> bool:
    try:
        response = requests.get(f'http://localhost:{port}/service/get-status')
    except requests.exceptions.ConnectionError:
        return False
    if response.status_code != 200:
        raise UnknownAppError
    if response.text != 'Frogtab Local is running':
        raise UnknownAppError
    return True

def post_stop(port: int) -> bool:
    try:
        response = requests.post(f'http://localhost:{port}/service/post-stop')
    except requests.exceptions.ConnectionError:
        return False
    if response.status_code != 204:
        raise UnknownAppError
    return True

def post_add_message(port: int, message: str) -> bool:
    try:
        response = requests.post(f'http://localhost:{port}/service/post-add-message', json={
            'message': message
        })
    except requests.exceptions.ConnectionError:
        raise NotRunningError
    if response.status_code != 200:
        raise UnknownAppError
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        raise UnknownAppError
    if not isinstance(response_json, dict) or 'success' not in response_json:
        raise UnknownAppError
    return response_json['success']