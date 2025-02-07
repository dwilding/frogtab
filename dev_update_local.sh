#!/bin/sh

REPO="$PWD"
cp LICENSE LICENSE_openpgp local/package
rm -rf local/package/frogtab/local_server/static
cp -r app local/package/frogtab/local_server/static

cd "$REPO/local/package/frogtab/local_server"
rm -rf templates
mkdir templates
mv static/index.html static/icon-*.html static/help.html templates

cd "$REPO/local/package/frogtab/local_server/templates"
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{ server_base }}\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
rm *.backup