#!/bin/sh

LOCAL="$(pwd)"
. .venv/bin/activate

cd "$LOCAL/package"
pip install twine
twine upload dist/*