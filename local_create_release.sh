#!/usr/bin/bash

cd local

rm -rf static
rm -rf __pycache__
rm -f Frogtab_backup.json

cp -r ../app static
cp ../LICENSE .
cp ../LICENSE_openpgp .

sed -i 's/data-save=\"browser\"/data-save=\"service\"/' static/index.html static/icon-*.html static/help.html
sed -i 's/data-vibe=\"\"/data-vibe=\"👽 Send to your inbox…\"/' static/help.html

zip -r frogtab_local_v1xx.zip . -x .gitignore
mv frogtab_local_v1xx.zip ..

cd ..