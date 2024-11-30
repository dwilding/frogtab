import sys
from lib import config, FrogtabLocalClient, RequestOutcome

if len(sys.argv) < 3:
    print('Usage: python send.py <label> <task>')
    sys.exit(1)
client = FrogtabLocalClient(config.port)
outcome = client.add_message(sys.argv[1], sys.argv[2])
if outcome in {RequestOutcome.NO_CONNECTION, RequestOutcome.UNEXPECTED_APP}:
    print(f'Error: Unable to connect to Frogtab Local on port {config.port}')
    sys.exit(1)
if outcome == RequestOutcome.APP_FAILURE:
    print(f'Error: Unable to send to Frogtab with label {sys.argv[1]}')
    print(f'(Connected to Frogtab Local on port {config.port})')
    sys.exit(1)