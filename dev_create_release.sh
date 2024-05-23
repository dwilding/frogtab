#!/usr/bin/bash

cd local

rm -rf __pycache__
rm -rf static

cp -r ../app static
cp ../LICENSE .
cp ../LICENSE_openpgp .

rm -r static/open
rm static/*.php
rm static/sitemap.xml

sed -i 's/data-registration=\"long\"/data-registration=\"short\"/' static/help.html
sed -i 's/data-vibe=\"\"/data-vibe=\"👽 Send to your inbox…\"/' static/help.html
sed -i 's/data-location=\"server\"/data-location=\"local\"/' static/send.html

zip -r frogtab_local_vyyyymm-betaxx.zip . -x .gitignore
mv frogtab_local_vyyyymm-betaxx.zip ..

cd ..