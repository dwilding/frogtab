#!/usr/bin/bash

cp LICENSE local
cp LICENSE_openpgp local
rm -rf local/static
cp -r app local/static
rm -rf local/__pycache__
rm -f local/Frogtab_backup.json

cd local/static
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-vibe=\"\"/data-vibe=\"👽 Send to your inbox…\"/' help.html
rm *.backup

cd ..
zip -r frogtab_local_v1xx.zip .
mv frogtab_local_v1xx.zip ..