#!/bin/bash

set -e

extra="https://raw.githubusercontent.com/dwilding/frogtab/refs/heads/server-install/extra"

cd /home/protected
wget -O install_frogtab.sh "$extra/install_frogtab.sh"
chmod +x install_frogtab.sh
./install_frogtab.sh /home/public --refresh

cd /home/public
wget -qO- "$extra/frogtab.com/public/.htaccess" >> .htaccess
wget -O sitemap.xml "$extra/frogtab.com/public/sitemap.xml"
sed -i'.backup' 's/data-registration=\"short\"/data-registration=\"long\"/' help.html
rm *.backup
