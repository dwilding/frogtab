#!/usr/bin/bash

cp -r app/* server/public

cd server/public
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab.com\"/data-server-base=\"\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-location=\"local\"/data-location=\"server\"/' send.html
rm *.backup

cd ../packages
composer install