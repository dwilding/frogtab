from pathlib import Path
from json import dump

working_dir = Path.cwd()
methods = {}
messages = {}

def backup(desc):
    def decorator(func):
        methods[func.__name__] = {
            'desc': desc,
            'func': func
        }
        return func
    return decorator

def list_methods():
    return [{
        'key': key,
        'desc': methods[key]['desc']
    } for key in methods.keys()]

def save_data(key, data):
    if (key not in methods):
        return {
            'success': False
        }
    method = methods[key]
    method['func'](data)
    return {
        'success': True
    }

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        dump(data, file, indent=2, ensure_ascii=False)

def add_message_for(instance_id, message):
    if instance_id not in messages:
        messages[instance_id] = []
    messages[instance_id].insert(0, message)
    return {
        'success': True
    }

def remove_messages_for(instance_id):
    if instance_id not in messages:
        messages[instance_id] = []
    num_messages = len(messages[instance_id])
    return {
        'success': True,
        'messages': [messages[instance_id].pop() for _ in range(num_messages)]
    }