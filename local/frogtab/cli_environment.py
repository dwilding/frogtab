from pathlib import Path

import sys
import os


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