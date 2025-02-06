from pathlib import Path

import sys
import os

import frogctl

def main():
    args = sys.argv[1:]
    if args == ['--version'] or args == ['-V']:
        print(f'Frogtab Local {frogctl.__version__}')
        return
    if args == ['help'] or args == ['--help'] or args == ['-h']:
        # TODO: Show help
        return
    commands = Commands()
    if not args:
        commands.send()
        return
    if args == ['start']:
        commands.start()
        return
    if args == ['stop']:
        commands.stop()
        return
    if args == ['status']:
        commands.status()
        return
    if len(args) == 2 and args[0] == 'get':
        if args[1] == 'port':
            commands.get_port()
            return
        if args[1] == 'backup-file':
            commands.get_backup_file()
            return
        if args[1] == 'registration-server':
            commands.get_registration_server()
            return
    if len(args) == 3 and args[0] == 'set':
        if args[1] == 'port':
            try:
                port = int(args[2])
            except ValueError:
                print('Port must be an integer')
                sys.exit(2)
            if port < 1024:
                print('Port must be at least 1024')
                sys.exit(2)
            commands.set_port(port)
            return
        if args[1] == 'backup-file':
            commands.set_backup_file(str(args[2]))
            return
        if args[1] == 'registration-server':
            commands.set_registration_server(str(args[2]))
            return
    # TODO: Show usage
    sys.exit(2)


class Commands():
    def __init__(self):
        self.env = Environment()
        self.controller = frogctl.Controller(
            self.env.config_file,
            on_read_error=Commands._exit_on_read_error,
            on_write_error=Commands._exit_on_write_error
        )
        self.env.set_display_variables(f'http://localhost:{self.controller.port}')

    def start(self) -> None:
        try:
            started = self.controller.start()
        except frogctl.WrongAppError:
            self._exit_on_wrong_app()
        if started:
            print(f'{self.env.display_tick} Started Frogtab Local')
            print(f'To access Frogtab, open {self.env.display_url} in your browser')
        else:
            print(f'Frogtab Local is running on port {self.controller.port}')

    def stop(self) -> None:
        try:
            stopped = self.controller.stop()
        except frogctl.WrongAppError:
            self._exit_on_wrong_app()
        if stopped:
            print(f'{self.env.display_tick} Stopped Frogtab Local')
        else:
            print(f'Frogtab Local is not running on port {self.controller.port}')

    def status(self) -> None:
        try:
            running = self.controller.is_running()
        except frogctl.WrongAppError:
            self._exit_on_wrong_app()
        if not running:
            print(f'Frogtab Local is not running on port {self.controller.port}')
            sys.exit(1)
        print(f'Frogtab Local is running on port {self.controller.port}')

    def send(self) -> None:
        try:
            started = self.controller.start()
        except frogctl.WrongAppError:
            self._exit_on_wrong_app()
        task = self.env.get_task_or_exit()
        try:
            self.controller.send(task)
        except frogctl.NotRunningError:
            print(f'Unable to send task to Frogtab because Frogtab Local is not running on port {self.controller.port}')
            sys.exit(1)
        except frogctl.WrongAppError:
            print(f'Unable to send task to Frogtab because a different app is using port {self.controller.port}')
            sys.exit(1)
        if started:
            print(f'{self.env.display_tick} Started Frogtab Local and sent task to Frogtab')
            print(f'To access Frogtab, open {self.env.display_url} in your browser')
        else:
            print(f'{self.env.display_tick} Sent task to Frogtab')

    def get_port(self) -> None:
        print(self.controller.port)

    def get_backup_file(self) -> None:
        print(self.controller.backup_file)

    def get_registration_server(self) -> None:
        print(self.controller.registration_server)

    def set_port(self, port: int) -> None:
        current_port = self.controller.port
        if port == current_port:
            print(f'Frogtab Local is already configured to use port {port}')
            return
        try:
            self.controller.set_port(port)
        except frogctl.RunningError:
            print(f'Frogtab Local is running on port {self.controller.port}')
            print('Stop Frogtab Local before changing the port')
            sys.exit(1)
        print(f'{self.env.display_tick} Changed port from {current_port} to {port}')

    def set_backup_file(self, backup_file: str) -> None:
        current_backup_file = self.controller.backup_file
        if backup_file == current_backup_file:
            print(f'Frogtab Local is already configured to use backup file \'{backup_file}\'')
            return
        try:
            self.controller.set_backup_file(backup_file)
        except frogctl.RunningError:
            print(f'Frogtab Local is running on port {self.controller.port}')
            print('Stop Frogtab Local before changing the backup file')
            sys.exit(1)
        print(f'{self.env.display_tick} Changed backup file from \'{current_backup_file}\' to \'{backup_file}\'')

    def set_registration_server(self, registration_server: str) -> None:
        current_registration_server = self.controller.registration_server
        if registration_server == current_registration_server:
            print(f'Frogtab Local is already configured to use registration server \'{registration_server}\'')
            return
        try:
            self.controller.set_registration_server(registration_server)
        except frogctl.RunningError:
            print(f'Frogtab Local is running on port {self.controller.port}')
            print('Stop Frogtab Local before changing the registration server')
            sys.exit(1)
        print(f'{self.env.display_tick} Changed registration server from \'{current_registration_server}\' to \'{registration_server}\'')

    def _exit_on_wrong_app(self):
        print(f'A different app is using port {self.controller.port}')
        sys.exit(1)

    @staticmethod
    def _exit_on_read_error(file: str):
        print(f'Unable to read file \'{file}\'')
        sys.exit(13)

    @staticmethod
    def _exit_on_write_error(file: str):
        print(f'Unable to write file \'{file}\'')
        sys.exit(13)


class Environment():
    def __init__(self):
        self.tty_in = os.isatty(sys.stdin.fileno())
        self.tty_out = os.isatty(sys.stdout.fileno())
        self.config_file = os.getenv('FROGTAB_CONFIG_FILE')
        if not self.config_file:
            self.config_file = 'Frogtab_config.json'
        if not Path(self.config_file).is_file():
            pass # TODO: Try creating from legacy config

    def set_display_variables(self, url: str) -> None:
        self.display_url = url
        self.display_tick = '✓'
        if self.tty_out and not os.getenv('NO_COLOR'):
            self.display_url = f'\033[96m{self.display_url}\033[0m' # bright cyan
            self.display_tick = f'\033[32m{self.display_tick}\033[0m' # green

    def get_task_or_exit(self) -> str:
        task = ''
        if self.tty_in:
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
        return task


if __name__ == '__main__':
    main()