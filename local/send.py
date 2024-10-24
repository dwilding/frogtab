import sys
import requests

try:
    from config import local_port
except ImportError:
    local_port = 5000

if len(sys.argv) < 3:
    print('Usage: python3 send.py <id> <task>')
    sys.exit(1)

url = f'http://127.0.0.1:{local_port}/service/post-add-message'
body = {
    'instance_id': sys.argv[1],
    'message': sys.argv[2]
}

try:
    requests.post(url, json=body)
except requests.exceptions.ConnectionError:
    print('Error: Frogtab Local is not running')
    sys.exit(1)