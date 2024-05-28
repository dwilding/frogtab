from functions import backup
from json import dump

@backup('Save to Frogtab_backup.json')
def save_file(data):
    with open('Frogtab_backup.json', 'w', encoding='utf-8') as file:
        dump(data, file, indent=2, ensure_ascii=False)