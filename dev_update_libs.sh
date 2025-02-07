#!/bin/sh

wget -O app/simple.min.css "https://cdn.simplecss.org/simple.min.css"
wget -O app/openpgp.min.mjs "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs"
wget -O LICENSE_openpgp "https://raw.githubusercontent.com/openpgpjs/openpgpjs/main/LICENSE"
cp LICENSE_openpgp local/package