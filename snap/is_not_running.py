from requests import get, exceptions
import sys

try:
    from config import local_port
except ImportError:
    local_port = 5000

try:
    response = get(f'http://127.0.0.1:{local_port}/service/get-methods')
except exceptions.ConnectionError:
    sys.exit(0)

if response.status_code != 200 or not isinstance(response.json(), list):
    print(f'Error: A different app is using port {local_port}')
    sys.exit(1)

print(f'Frogtab Local is running on http://127.0.0.1:{local_port}')
sys.exit(1)