import sys
from os import getenv, isatty
from subprocess import Popen, DEVNULL
from time import sleep
from urllib import parse
from enum import Enum
from configparser import ConfigParser
from json import dumps
from requests import get, post, exceptions


class Config():
    def __init__(self, file):
        self.load_external(file)
        # TODO: Verify that backup file can be written (by trying to write it?)
        self.set_flask_config()
        self.local_host = f'http://127.0.0.1:{self.local_port}'
        self.url_display = self.local_host
        self.tick_display = '✓'
        if not getenv('NO_COLOR'):
            self.tick_display = f'\033[32m{self.tick_display}\033[0m' # Make the tick green
            self.url_display = f'\033[96m{self.url_display}\033[0m' # Make the URL bright cyan

    def load_external(self, file):
        # TODO: Check that file exists
        config = ConfigParser()
        config.read(file)
        # TODO: Handle missing data in the config
        self.local_port = config['Frogtab Local']['local_port']
        self.registration_server = config['Frogtab Local']['registration_server']
        # TODO: Override config if environment variables are set

    def set_flask_config(self):
        self.flask_script = getenv('FROGTAB_FLASK_SCRIPT')
        if not self.flask_script:
            self.flask_script = 'frogtab_flask.py'
        self.flask_config = dumps({
            'local_port': self.local_port,
            'registration_server': self.registration_server
        }, ensure_ascii=False)


config = Config('config.ini')


def main():
    args = sys.argv[1:]
    if not args or args == ['start']:
        Command.start()
    if args == ['-V'] or args == ['--version']:
        print('Frogtab Local v2.00')
        sys.exit(0)
    if args == ['-h'] or args == ['--help'] or args == ['help']:
        print('Help: TODO')
        sys.exit(0)
    if args == ['status']:
        Command.status()
    if args == ['stop']:
        Command.stop()
    if len(args) == 1 and args[0] == 'send':
        Command.send_from_stdin()
    if len(args) == 2 and args[0] == 'send':
        Command.send(args[1])
    print('Usage: TODO')
    sys.exit(2)


class ServiceStatus(Enum):
    SERVICE_RUNNING = f'''Frogtab Local is running on port {config.local_port}
To access Frogtab, open {config.url_display} in your browser'''
    NO_CONNECTION = f'Frogtab Local is not running on port {config.local_port}'
    UNEXPECTED_APP = f'A different app is using port {config.local_port}'


class Service():
    @staticmethod
    def probe() -> ServiceStatus:
        try:
            response = get(f'{config.local_host}/service/get-methods')
        except exceptions.ConnectionError:
            return ServiceStatus.NO_CONNECTION
        if response.status_code != 200:
            return ServiceStatus.UNEXPECTED_APP
        response_json = response.json()
        try:
            response_json = response.json()
        except exceptions.JSONDecodeError:
            return ServiceStatus.UNEXPECTED_APP
        if not isinstance(response_json, list):
            return ServiceStatus.UNEXPECTED_APP
        return ServiceStatus.SERVICE_RUNNING

    @staticmethod
    def wait(test) -> ServiceStatus:
        delay = 0.2
        for attempt in range(4):
            sleep(delay)
            status = Service.probe()
            if test(status):
                break
            delay *= 2
        return status

    @staticmethod
    def start() -> ServiceStatus:
        Popen([
            'python',
            config.flask_script,
            config.flask_config
        ], stdout=DEVNULL)
        return Service.wait(lambda status: status == ServiceStatus.SERVICE_RUNNING)


class Command():
    @staticmethod
    def status():
        status = Service.probe()
        if status in {ServiceStatus.SERVICE_RUNNING, ServiceStatus.NO_CONNECTION}:
            print(status.value)
            sys.exit(0)
        print(status.value)
        sys.exit(1)

    @staticmethod
    def start():
        status = Service.probe()
        if status == ServiceStatus.NO_CONNECTION:
            started_status = Service.start()
            if started_status == ServiceStatus.SERVICE_RUNNING:
                print(f'''{config.tick_display} Started Frogtab Local
To access Frogtab, open {config.url_display} in your browser''')
                sys.exit(0)
            if started_status == ServiceStatus.NO_CONNECTION:
                print(f'Unable to start Frogtab Local (port {config.local_port})')
                sys.exit(1)
            print(started_status.value)
            sys.exit(1)
        if status == ServiceStatus.SERVICE_RUNNING:
            print(status.value)
            sys.exit(0)
        print(status.value)
        sys.exit(1)

    @staticmethod
    def stop():
        try:
            response = post(f'{config.local_host}/service/post-stop')
        except exceptions.ConnectionError:
            print(ServiceStatus.NO_CONNECTION.value)
            sys.exit(0)
        if response.status_code != 204:
            print(ServiceStatus.UNEXPECTED_APP.value)
            sys.exit(1)
        stopped_status = Service.wait(lambda status: status != ServiceStatus.SERVICE_RUNNING)
        if stopped_status == ServiceStatus.NO_CONNECTION:
            print(f'{config.tick_display} Stopped Frogtab Local')
            sys.exit(0)
        if stopped_status == ServiceStatus.SERVICE_RUNNING:
            print(f'Unable to stop Frogtab Local (port {config.local_port})')
            sys.exit(1)
        print(stopped_status.value)
        sys.exit(1)

    @staticmethod
    def send(task):
        try:
            response = post(f'{config.local_host}/service/post-add-message', json={
                'message': task
            })
        except exceptions.ConnectionError:
            Command.start_then_send(task) # Also calls sys.exit()
        if response.status_code != 200:
            print(ServiceStatus.UNEXPECTED_APP.value)
            sys.exit(1)
        try:
            response_json = response.json()
        except exceptions.JSONDecodeError:
            print(ServiceStatus.UNEXPECTED_APP.value)
            sys.exit(1)
        if not isinstance(response_json, dict) or 'success' not in response_json:
            print(ServiceStatus.UNEXPECTED_APP.value)
            sys.exit(1)
        if not response_json['success']:
            print(f'Unable to send task to Frogtab (port {config.local_port})')
            sys.exit(1)
        print(f'{config.tick_display} Sent task to Frogtab')
        sys.exit(0)

    @staticmethod
    def start_then_send(task):
        started_status = Service.start()
        if started_status == ServiceStatus.SERVICE_RUNNING:
            try:
                response = post(f'{config.local_host}/service/post-add-message', json={
                    'message': task
                })
            except exceptions.ConnectionError:
                print(ServiceStatus.NO_CONNECTION.value)
                sys.exit(1)
            if response.status_code != 200:
                print(ServiceStatus.UNEXPECTED_APP.value)
                sys.exit(1)
            try:
                response_json = response.json()
            except exceptions.JSONDecodeError:
                print(ServiceStatus.UNEXPECTED_APP.value)
                sys.exit(1)
            if not isinstance(response_json, dict) or 'success' not in response_json:
                print(ServiceStatus.UNEXPECTED_APP.value)
                sys.exit(1)
            if not response_json['success']:
                print(f'Unable to send task to Frogtab (port {config.local_port})')
                sys.exit(1)
            print(f'''{config.tick_display} Started Frogtab Local and sent task to Frogtab
To access Frogtab, open {config.url_display} in your browser''')
            sys.exit(0)
        if started_status == ServiceStatus.NO_CONNECTION:
            print(f'Unable to start Frogtab Local (port {config.local_port})')
            sys.exit(1)
        print(started_status.value)
        sys.exit(1)

    @staticmethod
    def send_from_stdin():
        task = ''
        if isatty(sys.stdin.fileno()):
            try:
                task = input("> ")
            except KeyboardInterrupt:
                sys.exit(130)
            except EOFError:
                print()
                sys.exit(1)
        else:
            task = sys.stdin.read()
        if task:
            Command.send(task) # Also calls sys.exit()
        sys.exit(1)


if __name__ == '__main__':
    main()