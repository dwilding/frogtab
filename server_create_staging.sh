#!/usr/bin/bash

shopt -s dotglob

rm -rf staging
mkdir staging
cp -r server/* staging
cp -r app/* staging

sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab.com\"/data-server-base=\"\"/' staging/index.html staging/icon-*.html staging/help.html
sed -i'.backup' 's/data-location=\"local\"/data-location=\"server\"/' staging/send.html
rm staging/*.backup