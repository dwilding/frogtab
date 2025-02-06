#!/bin/sh

LOCAL="$(pwd)"
. .venv/bin/activate

cd "$LOCAL/python"
twine upload dist/*