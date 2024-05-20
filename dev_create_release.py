#!/usr/bin/python3

# This script creates a local version of Frogtab and packages it for release

from pathlib import Path
import shutil, os

def replace_string(file_path, search, replacement):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    file_contents = file_contents.replace(search, replacement)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_contents)

# Make a full copy of the app
local_app_dir = Path('local/app')
if local_app_dir.exists():
    shutil.rmtree(local_app_dir)
shutil.copytree(Path('app'), local_app_dir)

# Remove files that are not needed locally
shutil.rmtree(Path('local/app/open'))
for file_path in Path('local/app').glob('*.php'):
    file_path.unlink()
Path('local/app/sitemap.xml').unlink()

# Enable the short registration flow
replace_string('local/app/help.html', 'data-registration="long"', 'data-registration="short"')
replace_string('local/app/help.html', 'data-vibe=""', 'data-vibe="👽 Send to your inbox…"')

# Disable local versions of personal links
replace_string('local/app/send.html', 'data-location="server"', 'data-location="local"')

# Package the local version as a ZIP file
os.system('cd local; zip -r frogtab_local_vyyyymm-betaxx.zip . -x .gitignore; mv frogtab_local_vyyyymm-betaxx.zip ..')