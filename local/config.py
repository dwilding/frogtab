from frogtab_helpers import working_dir, backup, write_json

local_port = 5000

@backup(f'Save file to {working_dir}')
def save_file(data):
    write_json(data, 'Frogtab_backup.json')