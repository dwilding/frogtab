#!/bin/bash

shopt -s dotglob

ROOT_PRIVATE=/home/private
ROOT_PROTECTED=/home/protected
ROOT_PUBLIC=/home/public

cd $ROOT_PRIVATE
rm -rf frogtab
git clone git@github.com:dwilding/frogtab.git

cd $ROOT_PRIVATE/frogtab
rm -rf $ROOT_PROTECTED/installed
mkdir $ROOT_PROTECTED/installed
cp -r server app build_server.sh $ROOT_PROTECTED/installed

cd $ROOT_PROTECTED/installed
./build_server.sh
rm -rf app build_server.sh

cd $ROOT_PROTECTED/installed/server/public
cat $ROOT_PRIVATE/frogtab/development/frogtab.com/.htaccess >> .htaccess
cp $ROOT_PRIVATE/frogtab/development/frogtab.com/sitemap.xml .
sed -i'.backup' 's/data-registration=\"short\"/data-registration=\"long\"/' help.html
rm *.backup
rm -rf $ROOT_PUBLIC/*
cp -r * $ROOT_PUBLIC

cd $ROOT_PROTECTED/installed/server
rm -rf public

cd $ROOT_PRIVATE
rm -rf frogtab
