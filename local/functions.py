from json import dump

methods = {}

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

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        dump(data, file, indent=2, ensure_ascii=False)