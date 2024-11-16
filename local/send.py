from requests import post, exceptions
import sys

try:
    from config import local_port
except ImportError:
    local_port = 5000

if len(sys.argv) < 3:
    print('Usage: python send.py <label> <task>')
    sys.exit(1)

url = f'http://127.0.0.1:{local_port}/service/post-add-message'
body = {
    'instance_id': sys.argv[1],
    'message': sys.argv[2]
}

try:
    response = post(url, json=body)
except exceptions.ConnectionError:
    print(f'Error: Frogtab Local is not running on http://127.0.0.1:{local_port}')
    sys.exit(1)

if response.status_code != 200:
    print(f'Error: Frogtab Local is not running on http://127.0.0.1:{local_port}')
    sys.exit(1)

if not response.json()['success']:
    print(f'Error: Unable to send to Frogtab with label {sys.argv[1]}')
    sys.exit(1)