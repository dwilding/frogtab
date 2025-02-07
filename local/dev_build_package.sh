#!/bin/sh

LOCAL="$PWD"
rm -rf package/frogtab/local_server/static
cp -r --dereference app package/frogtab/local_server/static

cd "$LOCAL/package/frogtab/local_server"
rm -rf templates
mkdir templates
mv static/index.html static/icon-*.html static/help.html templates

cd "$LOCAL/package/frogtab/local_server/templates"
sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{ server_base }}\"/' index.html icon-*.html help.html
sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
rm *.backup

cd "$LOCAL"
mkdir -p testing
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate

cd "$LOCAL/package"
rm -rf dist
rm -rf frogtab.egg-info
pip install build
python -m build
pip install dist/frogtab-*.whl