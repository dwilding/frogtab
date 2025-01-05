from pathlib import Path
from json import dump


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
        return {
            'success': True
        }

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
        dump(data, file, indent=2, ensure_ascii=False)