#!/bin/sh

LOCAL="$PWD"
. .venv/bin/activate

cd "$LOCAL/package"
pip install twine
twine upload dist/*