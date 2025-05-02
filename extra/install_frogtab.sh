#!/bin/bash

set -e
shopt -s dotglob

protected="$PWD"
public="$1"
if [ -z "$public" ]; then
  echo "Error: no public directory specified"
  exit 2
fi
if [ ! -d "$public" ]; then
  echo "Error: directory '$public' does not exist"
  exit 1
fi
if [ ! "$2" = "--refresh" ] && [ -n "$(find "$public" -mindepth 1 -print -quit)" ]; then
  echo "Error: directory '$public' is not empty"
  exit 1
fi
if [ "$2" = "--refresh" ]; then
  rm -rf frogtab
fi
if [ -d "frogtab" ]; then
  echo "Error: directory '$protected/frogtab' already exists"
  exit 1
fi
wget -O frogtab.zip "https://github.com/dwilding/frogtab/archive/refs/heads/server-install.zip"
unzip frogtab.zip -d frogtab
rm frogtab.zip

cd "$protected/frogtab"
mkdir src
mv frogtab-server-install/app frogtab-server-install/server src

cd "$protected/frogtab/src"
"$protected/frogtab/frogtab-server-install/scripts/build_server.sh" "$protected/frogtab.db"
rm -rf "$protected/frogtab/frogtab-server-install"
rm -rf app
if [ "$2" = "--refresh" ]; then
  rm -rf "$public"/*
fi
mv server/public/* "$public"
