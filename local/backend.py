services = {}

def service(desc):
    def decorator(func):
        services[func.__name__] = {
            'desc': desc,
            'func': func
        }
        return func
    return decorator

def list_services():
    return [{
        'key': key,
        'desc': services[key]['desc']
    } for key in services.keys()]

def call_service(key, data):
    service = services[key]
    service['func'](data)