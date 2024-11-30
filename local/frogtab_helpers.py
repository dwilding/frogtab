from pathlib import Path
from json import dump


working_dir = Path.cwd()


def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        dump(data, file, indent=2, ensure_ascii=False)


class FrogtabLocalBackend():
    def __init__(self):
        self._methods = {}
        self._messages = {}

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

    def add_message_for(self, instance_id, message):
        if instance_id not in self._messages:
            return {
                'success': False
            }
        self._messages[instance_id].insert(0, message)
        return {
            'success': True
        }

    def remove_messages_for(self, instance_id):
        if instance_id not in self._messages:
            self._messages[instance_id] = []
        num_messages = len(self._messages[instance_id])
        removed_messages = [self._messages[instance_id].pop() for _ in range(num_messages)]
        return {
            'success': True,
            'messages': removed_messages
        }


backend = FrogtabLocalBackend()


# Defines the @backup decorator for use in config.py
def backup(desc):
    def decorator(func):
        backend.set_method(desc, func)
        return func
    return decorator