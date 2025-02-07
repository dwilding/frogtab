#!/bin/sh

LOCAL="$PWD"
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