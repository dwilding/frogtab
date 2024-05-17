# This script updates the ?sha1=... parameters in dependency references

import re
import subprocess

def sha1sum(file_path):
    output = subprocess.run(['sha1sum', file_path], capture_output=True, text=True)
    return output.stdout.split()[0]

def replace_ref(match):
    file_name = match.group(1)
    print(f'  - {file_name}')
    file_sha1sum = sha1sum(f'app/{file_name}')
    return f'{file_name}?sha1={file_sha1sum}'

def update_refs(file_name):
    print(file_name)
    refs_re = r'([\w.-]+)\?sha1=[0-9a-f]+'
    file_path = f'app/{file_name}'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    file_contents = re.sub(refs_re, replace_ref, file_contents)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_contents)
    print()

update_refs('main.js')
update_refs('index.html')
update_refs('icon-normal.html')
update_refs('icon-notify.html')
update_refs('help.html')
update_refs('achievements.html')
update_refs('send.html')
update_refs('week.html')