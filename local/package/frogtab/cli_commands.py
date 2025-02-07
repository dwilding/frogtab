import sys

from .cli_environment import Environment
from .controller import Controller, WrongAppError, WrongVersionError, NotRunningError, RunningError


class Commands():
    def __init__(self):
        self.env = Environment()
        self.controller = Controller(
            self.env.config_file,
            on_read_error=Commands._exit_on_read_error,
            on_write_error=Commands._exit_on_write_error
        )
        self.env.set_display_variables(f'http://localhost:{self.controller.port}')

    def start(self) -> None:
        try:
            started = self.controller.start()
        except WrongAppError:
            self._exit_on_wrong_app()
        except WrongVersionError:
            self._exit_on_wrong_version()
        if started:
            print(f'{self.env.display_tick} Started Frogtab Local')
            print(f'To access Frogtab, open {self.env.display_url} in your browser')
        else:
            print(f'Frogtab Local is running on port {self.controller.port}')

    def stop(self) -> None:
        try:
            stopped = self.controller.stop()
        except WrongAppError:
            self._exit_on_wrong_app()
        if stopped:
            print(f'{self.env.display_tick} Stopped Frogtab Local')
        else:
            print(f'Frogtab Local is not running on port {self.controller.port}')

    def status(self) -> None:
        try:
            running = self.controller.is_running()
        except WrongAppError:
            self._exit_on_wrong_app()
        except WrongVersionError:
            self._exit_on_wrong_version()
        if not running:
            print(f'Frogtab Local is not running on port {self.controller.port}')
            sys.exit(1)
        print(f'Frogtab Local is running on port {self.controller.port}')

    def send(self) -> None:
        try:
            started = self.controller.start()
        except WrongAppError:
            self._exit_on_wrong_app()
        except WrongVersionError:
            self._exit_on_wrong_version()
        task = self.env.get_task_or_exit()
        try:
            self.controller.send(task)
        except NotRunningError:
            print(f'Unable to send task to Frogtab because Frogtab Local is not running on port {self.controller.port}')
            sys.exit(1)
        except WrongAppError:
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
        except RunningError:
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
        except RunningError:
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
        except RunningError:
            print(f'Frogtab Local is running on port {self.controller.port}')
            print('Stop Frogtab Local before changing the registration server')
            sys.exit(1)
        print(f'{self.env.display_tick} Changed registration server from \'{current_registration_server}\' to \'{registration_server}\'')

    def _exit_on_wrong_app(self):
        print(f'A different app is using port {self.controller.port}')
        sys.exit(1)

    def _exit_on_wrong_version(self):
        print(f'The wrong version of Frogtab Local is running on port {self.controller.port}')
        sys.exit(1)

    @staticmethod
    def _exit_on_read_error(file: str):
        print(f'Unable to read file \'{file}\'')
        sys.exit(13)

    @staticmethod
    def _exit_on_write_error(file: str):
        print(f'Unable to write file \'{file}\'')
        sys.exit(13)