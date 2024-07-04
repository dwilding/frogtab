#!/bin/sh

DIR_CALLER="$(pwd)"

cd "$(dirname "$0")" # cd to repo root
cp -r app/* server/public
DIR_PACKAGES="$(pwd)/server/packages"

cd server/public
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab.com\"/data-server-base=\"\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-location=\"local\"/data-location=\"server\"/' send.html
rm *.backup
cat <<EOF > .htaccess
SetEnv DIR_PACKAGES "$DIR_PACKAGES"
SetEnv FILE_SQLITEDB "$DIR_CALLER/frogtab.db"
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^([^\.]+)$ $1.php [L]
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^([^\.]+)$ $1.html [L]
EOF

cd ../packages
composer install

cd "$DIR_CALLER"