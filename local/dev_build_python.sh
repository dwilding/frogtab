#!/bin/sh

LOCAL="$(pwd)"
. .venv/bin/activate

cd "$LOCAL/python"
rm -rf dist
rm -rf frogtab.egg-info
python -m build