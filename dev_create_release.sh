#!/bin/sh

cp LICENSE LICENSE_openpgp local
rm -rf local/static
cp -r app local/static
rm -rf local/__pycache__
rm -f local/Frogtab_backup.json

cd local/static
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
rm *.backup

cd ..
zip -r frogtab_local_v1xx.zip .
mv frogtab_local_v1xx.zip ..

cd ..
rm -rf snapcraft
cp -r local snapcraft
rm -f snapcraft/README.md
rm -f snapcraft/CHANGELOG.md
cp -r snap/* snapcraft

cd snapcraft
mkdir flask
mv static app.py frogtab_helpers.py requirements.txt flask
snapcraft pack
mv frogtab_*.snap ..

cd ..