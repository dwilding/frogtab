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
    method = methods[key]
    method['func'](data)