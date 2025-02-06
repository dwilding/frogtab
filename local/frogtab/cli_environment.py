from pathlib import Path

import sys
import os
import shutil
import subprocess


class Environment():
    def __init__(self):
        self.tty_in = os.isatty(sys.stdin.fileno())
        self.tty_out = os.isatty(sys.stdout.fileno())
        self.config_file = os.getenv('FROGTAB_CONFIG_FILE')
        if not self.config_file:
            self.config_file = 'Frogtab_config.json'
        if not Path(self.config_file).is_file():
            self.try_migrate_legacy_config()

    def try_migrate_legacy_config(self) -> None:
        if not Path('config.py').is_file() or Path('migrated').exists():
            return
        # Move config.py to a dedicated subdir of the working dir
        shutil.copytree(Path(__file__).parent / 'legacy', 'migrated')
        shutil.move('config.py', 'migrated')
        # Read config.py and create a JSON file
        config_file = Path('migrated') / 'Frogtab_config.json'
        result = subprocess.run([
            'python',
            Path('migrated') / 'migrate_config.py',
            config_file
        ])
        # Copy the JSON file to the correct location
        if config_file.is_file():
            shutil.copy(config_file, self.config_file)

    def set_display_variables(self, url: str) -> None:
        self.display_url = url
        self.display_tick = '✓'
        if self.tty_out and not os.getenv('NO_COLOR'):
            self.display_url = f'\033[96m{self.display_url}\033[0m' # Bright cyan
            self.display_tick = f'\033[32m{self.display_tick}\033[0m' # Green

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