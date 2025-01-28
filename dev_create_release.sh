#!/bin/sh

REPO=$(pwd)
cp LICENSE LICENSE_openpgp local
rm -rf local/local_server/static
cp -r app local/local_server/static

cd "$REPO/local"
rm -f Frogtab_backup.json
rm -f config.json
rm -f config.py
rm -rf migrated
rm -rf .venv
rm -rf __pycache__

cd "$REPO/local/local_server"
rm -rf templates
mkdir templates
mv static/index.html static/icon-*.html static/help.html templates
rm -rf __pycache__

cd "$REPO/local/local_server/templates"
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{ server_base }}\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
sed -i'.backup' 's/\(<a tabindex="0" href="https:\/\/github\.com\/dwilding\/frogtab"\)/<a tabindex="0" href="https:\/\/github.com\/dwilding\/frogtab\/releases\/tag\/v2.00" target="_blank">v2.00 release notes<\/a> • \1/' help.html
rm *.backup

cd "$REPO/local"
zip -r frogtab_local_v200.zip .
mv frogtab_local_v200.zip ..

cd "$REPO"
rm -rf snapcraft
cp -r local snapcraft
rm -f snapcraft/README.md
cp -r snap/* snapcraft

cd "$REPO/snapcraft"
mkdir src
mv local_server legacy cli.py client.py requirements.txt src

cd "$REPO/snapcraft/src/local_server/templates"
sed -i'.backup' 's/<code>python cli\.py<\/code>/the <code>frogtab<\/code> command/g' help.html
rm *.backup

cd "$REPO/snapcraft"
if [ "$1" != "--no-pack" ]; then
    snapcraft pack
    mv frogtab_*.snap ..
fi

cd "$REPO/local"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
deactivate

cd "$REPO"