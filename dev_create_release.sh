#!/bin/sh

cp LICENSE LICENSE_openpgp local
rm -rf local/static
cp -r app local/static

cd local
rm -rf templates
mkdir templates
mv static/index.html static/icon-*.html static/help.html templates
rm -rf .venv
rm -rf __pycache__
rm -f Frogtab_backup.json

cd templates
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{ server_base }}\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
sed -i'.backup' 's/\(<a tabindex="0" href="https:\/\/github\.com\/dwilding\/frogtab"\)/<a tabindex="0" href="https:\/\/github.com\/dwilding\/frogtab\/releases\/tag\/v2.00" target="_blank">v2.00 release notes<\/a> • \1/' help.html
rm *.backup

cd ..
zip -r frogtab_local_v200.zip .
mv frogtab_local_v200.zip ..

cd ..
rm -rf snapcraft
cp -r local snapcraft
rm -f snapcraft/README.md
cp -r snap/* snapcraft

cd snapcraft
mkdir src
mv static templates app.py frogtab_backend.py frogtab_flask.py requirements.txt src

cd src/templates
sed -i'.backup' 's/python app\.py/frogtab/g' help.html
rm *.backup

cd ../..
snapcraft pack
mv frogtab_*.snap ..

cd ../local
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
deactivate

cd ..