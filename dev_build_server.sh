#!/bin/sh

cp -r app/* server/public
DIR_PACKAGES="$(pwd)/server/packages"
DIR_PARENT="$(cd .. && pwd)"

cd server/public
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab.com\/\"/data-server-base=\"\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-location=\"local\"/data-location=\"server\"/' send.html
sed -i'.backup' 's/\(<a tabindex="0" href="https:\/\/github.com\/dwilding\/frogtab"\)/<a tabindex="0" href="https:\/\/snapcraft.io\/frogtab" target="_blank">Frogtab on Linux<\/a> • \1/' help.html
rm *.backup
cat <<EOF > .htaccess
SetEnv DIR_PACKAGES "$DIR_PACKAGES"
SetEnv FILE_SQLITEDB "$DIR_PARENT/frogtab.db"
AddType text/javascript .mjs
RewriteEngine On
RewriteRule ^key_([0-9a-f-]{36})\.asc$ get-public-key.php?user_id=\$1 [L]
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^([^\.]+)$ \$1.php [L]
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^([^\.]+)$ \$1.html [L]
EOF

cd ../packages
composer install

cd ../..