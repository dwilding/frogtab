#!/bin/sh

cd "$SNAP_USER_COMMON"
if test ! -e config.py; then
  cp "$SNAP/config.py" .
fi
export PYTHONPATH=".:$PYTHONPATH"
"$SNAP/bin/python3" "$SNAP/flask/app.py" > /dev/null