# Before version 2.0.0, Frogtab Local imported config from config.py in the working dir.
# 
# config.py defines:
#   - local_port
#   - registration_server
#   - backup_file via save_file()
# 
# This script tries to import the config values from config.py and create a JSON file.
# 
# config.py expects to import helpers from frogtab_helpers:
#   - working_dir
#   - write_json()
#   - @backup()
# 
# We've mocked frogtab_helpers.py so that write_json() captures backup_file.
# 
# For an example of config.py, see:
# https://raw.githubusercontent.com/dwilding/frogtab/f5f2d5436440d9e6eb4af4aadfd7273a95b5cadc/local/config.py

from pathlib import Path
import sys
import json

args = sys.argv[1:]
config_path = Path(args[0])
config_dict = {
    "port": 5000,
    "expose": False,
    "backupFile": "Frogtab_backup.json",
    "registrationServer": "https://frogtab.com/",
    "internalState": {
        "pairingKey": "",
        "messages": []
    }
}
try:
    from config import local_port
    config_dict["port"] = local_port
except ImportError:
    pass
try:
    from config import registration_server
    config_dict["registrationServer"] = registration_server
except ImportError:
    pass
try:
    from config import save_file
    data = {}
    save_file(data) # capture the backup file path
    config_dict["backupFile"] = data["file_path"]
except ImportError:
    pass
content = json.dumps(config_dict, indent=2, ensure_ascii=False)
config_path.write_text(content, encoding="utf-8")