from frogtab_helpers import working_dir, backup, write_json


# Specifies the port that you'll use when accessing Frogtab in your browser
local_port = 5000


# You can customize the built-in backup method or add more backup methods
#
# The format of a backup method is
#
#   @backup('Name of backup method')
#   def unique_identifier(data):
#       do_something(data)
#
# where `data` is a dictionary that contains the backup data from your browser

@backup(f'Save file to {working_dir}')
def save_file(data):
    write_json(data, 'Frogtab_backup.json')


# Specifies the server that Frogtab uses if you register for a personal link
registration_server = 'https://frogtab.com/'