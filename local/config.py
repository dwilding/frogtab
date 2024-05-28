from functions import backup, write_json

@backup('Save to Frogtab_backup.json')
def save_file(data):
    write_json(data, 'Frogtab_backup.json')