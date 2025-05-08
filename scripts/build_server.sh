#!/bin/sh

set -e

repo="$PWD"
database="$1"
if [ -z "$database" ]; then
  echo "Error: no database path specified"
  exit 2
fi
settings="$2"
if [ -z "$settings" ]; then
  echo "Error: no settings path specified"
  exit 2
fi
cp -r app/* server/public

cd "$repo/server/public"
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-location=\"local\"/data-location=\"server\"/' send.html
sed -i'.backup' 's/\(<a tabindex="0" href="https:\/\/github\.com\/dwilding\/frogtab"\)/<a tabindex="0" href="https:\/\/snapcraft.io\/frogtab" target="_blank">Linux snap<\/a> • \1/' help.html
rm *.backup
cat <<EOF > .htaccess
SetEnv DIR_PACKAGES "$repo/server/packages"
SetEnv FILE_SQLITEDB "$database"
SetEnv FILE_SETTINGS "$settings"
AddType text/javascript .mjs
RewriteEngine On
RewriteRule ^key_([0-9a-f-]{36})\.asc$ get-public-key.php?user_id=\$1 [L]
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^([^\.]+)$ \$1.php [L]
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^([^\.]+)$ \$1.html [L]
EOF

cd "$repo/server/packages"
composer install

cd "$repo/server/public"
