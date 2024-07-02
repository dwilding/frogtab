#!/usr/bin/bash

cp -r app/* server
sed -i 's/data-server-base=\"https:\/\/frogtab.com\"/data-server-base=\"\"/' server/index.html server/icon-*.html server/help.html
sed -i 's/data-location=\"local\"/data-location=\"server\"/' server/send.html