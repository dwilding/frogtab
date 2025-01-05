from dataclasses import dataclass
from json import load, dump


@dataclass
class Config:
    config_file: str
    backup_file: str = 'Frogtab_backup.json'
    local_port: int = 5000
    registration_server: str = 'https://frogtab.com/'

    def fetch(self):
        with open(self.config_file, 'r', encoding='utf-8') as file:
            config_dict = load(file)
        if 'backupFile' in config_dict:
            self.backup_file = config_dict['backupFile']
        if 'localPort' in config_dict:
            self.local_port = config_dict['localPort']
        if 'registrationServer' in config_dict:
            self.registration_server = config_dict['registrationServer']

    def store(self):
        config_dict = {
            'backupFile': str(self.backup_file),
            'localPort': self.local_port,
            'registrationServer': self.registration_server
        }
        with open(self.config_file, 'w', encoding='utf-8') as file:
            dump(config_dict, file, indent=2, ensure_ascii=False)