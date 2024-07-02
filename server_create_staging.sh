#!/usr/bin/bash

rm -rf staging
cp -r server/* staging
cp -r app/* staging

sed -i 's/data-server-base=\"https:\/\/frogtab.com\"/data-server-base=\"\"/' staging/index.html staging/icon-*.html staging/help.html
sed -i 's/data-location=\"local\"/data-location=\"server\"/' staging/send.html