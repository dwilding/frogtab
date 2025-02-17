from pathlib import Path

working_dir = Path.cwd()

def write_json(data, file_path):
    data["file_path"] = file_path

def backup(desc):
    def decorator(func):
        return func
    return decorator