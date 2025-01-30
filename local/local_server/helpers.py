from pathlib import Path

import json


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.read()

    def read(self):
        with open(self.config_file, 'r', encoding='utf-8') as file:
            config_dict = json.load(file)
            self.port = config_dict['port']
            self.backup_file = config_dict['backupFile']
            self.registration_server = config_dict['registrationServer']

    def write(self):
        config_dict = {
            'port': self.port,
            'backupFile': str(self.backup_file),
            'registrationServer': self.registration_server
        }
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(config_dict, file, indent=2, ensure_ascii=False)


class AppBackend():
    def __init__(self):
        self._methods = {}
        self._messages = []

    def set_method(self, desc, func):
        self._methods[func.__name__] = {
            'desc': desc,
            'func': func
        }

    def methods(self):
        return [{
            'key': key,
            'desc': self._methods[key]['desc']
        } for key in self._methods.keys()]

    def save_data(self, key, data):
        if (key not in self._methods):
            return {
                'success': False
            }
        method = self._methods[key]
        method['func'](data)
        return {
            'success': True
        }

    def add_message(self, message):
        self._messages.insert(0, message)

    def remove_messages(self):
        num_messages = len(self._messages)
        removed_messages = [self._messages.pop() for _ in range(num_messages)]
        return {
            'success': True,
            'messages': removed_messages
        }


backend = AppBackend()


def backup(desc):
    def decorator(func):
        backend.set_method(desc, func)
        return func
    return decorator


@backup(f'Save file to {Path.cwd()}')
def save_file(data):
    with open('Frogtab_backup.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)