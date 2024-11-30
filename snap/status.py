import sys
from lib import config, FrogtabLocalClient, RequestOutcome

client = FrogtabLocalClient(config.port)
outcome = client.probe()
if outcome == RequestOutcome.NO_CONNECTION:
    sys.exit(2)
if outcome == RequestOutcome.UNEXPECTED_APP:
    print(f'Error: A different app is using port {config.port}')
    sys.exit(1)
print(f'Frogtab Local is running on http://127.0.0.1:{config.port}')