#/bin/sh

mkdir -p testing
python3 -m venv .venv
. .venv/bin/activate
pip install build
pip install twine