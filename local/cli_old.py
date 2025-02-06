from pathlib import Path

import sys
import os
import shutil
import subprocess
import json

import client

def main():
    args = sys.argv[1:]
    if not args:
        env = Environment()
        send_then_exit(env)
    if args == ['--version'] or args == ['-V']:
        print('Frogtab Local 2.0.0')
        sys.exit(0)
    if args == ['help'] or args == ['--help'] or args == ['-h']:
        print_help()
        sys.exit(0)
    if args == ['start']:
        env = Environment()
        start_then_exit(env)
    if args == ['stop']:
        env = Environment()
        stop_then_exit(env)
    if len(args) == 2 and args[0] == 'set-port' and args[1]:
        try:
            port = int(args[1])
        except ValueError:
            print('Port must be an integer')
            sys.exit(2)
        if port < 1024:
            print('Port must be at least 1024')
            sys.exit(2)
        env = Environment()
        if port == env.port:
            print(f'Frogtab Local is already configured to use port {port}')
            sys.exit(0)
        write_port_then_exit(env, port)
    print_usage()
    sys.exit(2)


class Environment:
    def __init__(self):
        self.set_default_config()
        self.config_file = os.getenv('FROGTAB_CONFIG_FILE')
        if not self.config_file:
            self.config_file = 'config.json'
        if Path(self.config_file).is_file():
            self.read_config() # TODO: What if the read fails?
        else:
            self.try_legacy_read_config()
            self.write_config() # TODO: What if the write fails?
        self.tty_in = os.isatty(sys.stdin.fileno())
        self.tty_out = os.isatty(sys.stdout.fileno())
        self.set_display_variables()

    def set_default_config(self):
        self.port = 5000
        self.backup_file = 'Frogtab_backup.json'
        self.registration_server = 'https://frogtab.com/'

    def set_config_from_dict(self, config: dict):
        if 'port' in config:
            self.port = config['port']
        if 'backupFile' in config:
            self.backup_file = config['backupFile']
        if 'registrationServer' in config:
            self.registration_server = config['registrationServer']

    def read_config(self):
        with open(self.config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        self.set_config_from_dict(config)

    def try_legacy_read_config(self):
        if not Path('config.py').is_file() or Path('migrated').exists():
            return
        # Move config.py to a dedicated subdir of the working dir
        shutil.copytree(Path(__file__).parent / 'legacy', 'migrated')
        shutil.move('config.py', 'migrated')
        result = subprocess.run(
            ['python', Path('migrated') / 'read_config.py'],
            capture_output=True,
            text=True
        )
        config = json.loads(result.stdout)
        self.set_config_from_dict(config)

    def write_config(self):
        config = {
            'port': self.port,
            'backupFile': self.backup_file,
            'registrationServer': self.registration_server
        }
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)

    def set_display_variables(self):
        self.display_url = f'http://localhost:{self.port}'
        self.display_tick = '✓'
        if self.tty_out and not os.getenv('NO_COLOR'):
            self.display_url = f'\033[96m{self.display_url}\033[0m' # bright cyan
            self.display_tick = f'\033[32m{self.display_tick}\033[0m' # green

    def start_server(self):
        self.write_config() # TODO: What if the write fails?
        subprocess.Popen([
            'python',
            Path(__file__).parent / 'local_server' / 'run.py',
            self.config_file
        ], stdout=subprocess.DEVNULL)


def send_then_exit(env: Environment):
    try:
        running = client.get_running(env.port)
    except client.UnknownAppError:
        exit_on_unknown_app(env)
    started = False
    if not running:
        start(env)
        started = True
    task = ''
    if env.tty_in:
        print('Add a task to your inbox:')
        try:
            task = input('> ')
        except KeyboardInterrupt:
            sys.exit(130)
        except EOFError:
            print()
            sys.exit(2)
    else:
        task = sys.stdin.read()
    if not task:
        sys.exit(2)
    try:
        client.post_add_message(env.port, task)
    except client.NotRunningError:
        print(f'Unable to send task to Frogtab because Frogtab Local is not running on port {env.port}')
        sys.exit(1)
    except client.UnknownAppError:
        exit_on_unknown_app()
    if started:
        print(f'''{env.display_tick} Started Frogtab Local and sent task to Frogtab
To access Frogtab, open {env.display_url} in your browser''')
    else:
        print(f'{env.display_tick} Sent task to Frogtab')
    sys.exit(0)

def exit_on_unknown_app(env: Environment):
    print(f'A different app is using port {env.port}')
    sys.exit(1)

def start(env: Environment):
    env.start_server()
    try:
        client.wait_for_running(env.port)
    except client.UnknownAppError:
        exit_on_unknown_app(env)

def start_then_exit(env: Environment):
    try:
        running = client.get_running(env.port)
    except client.UnknownAppError:
        exit_on_unknown_app(env)
    if running:
        print(f'Frogtab Local is running on port {env.port}')
    else:
        start(env)
        print(f'''{env.display_tick} Started Frogtab Local
To access Frogtab, open {env.display_url} in your browser''')
    sys.exit(0)

def stop_then_exit(env: Environment):
    try:
        submitted = client.post_stop(env.port)
    except client.UnknownAppError:
        exit_on_unknown_app(env)
    if not submitted:
        print(f'Frogtab Local is not running on port {env.port}')
        sys.exit(0)
    try:
        client.wait_for_not_running(env.port)
    except client.UnknownAppError:
        exit_on_unknown_app(env)
    print(f'{env.display_tick} Stopped Frogtab Local')
    sys.exit(0)

def write_port_then_exit(env: Environment, port: int):
    try:
        running = client.get_running(env.port)
    except client.UnknownAppError:
        running = False
    if running:
        print(f'''Frogtab Local is running on port {env.port}
Stop Frogtab Local before changing the port''')
        sys.exit(1)
    old_port = env.port
    env.port = port
    env.write_config() # TODO: What if this fails?
    print(f'{env.display_tick} Changed port from {old_port} to {port}')
    sys.exit(0)

def print_help():
    print('help') # TODO

def print_usage():
    print('usage') # TODO

if __name__ == '__main__':
    main()