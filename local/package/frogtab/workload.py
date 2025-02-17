from pathlib import Path
import sys
import subprocess

from . import client

def start(config_file: Path) -> bool:
    config = client._read_config(config_file)
    port = config["port"]
    if client.is_running(port):
        return False
    # Ensure that config file and backup file are writeable
    client._write_json(config, config_file)
    path_backup_file = Path(config["backupFile"])
    if path_backup_file.is_file():
        data = client._read_json(path_backup_file)
        client._write_json(data, path_backup_file)
    else:
        client._write_json({}, path_backup_file)
    # Run the server as a separate Python process
    subprocess.Popen([
        sys.executable,
        Path(__file__).parent / "local_server" / "server.py",
        config_file
    ], stdout=subprocess.DEVNULL)
    client._wait_for_connection(port)
    return True