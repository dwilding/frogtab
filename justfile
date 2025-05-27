_default:
  @just --list --unsorted

# 1️⃣  Build the package
[working-directory: "local"]
package: app licenses ruff _package-stage _package-build
  mkdir -p testing
  @echo ""
  @echo "To try the package:"
  @echo "  $ cd local"
  @echo "  $ . .venv/bin/activate"
  @echo "  $ cd testing"
  @echo "  $ frogtab ..."

[working-directory: "local"]
_package-build:
  #!/bin/sh
  rm -rf .venv
  python3 -m venv .venv
  . .venv/bin/activate
  cd package
  rm -rf dist
  rm -rf frogtab.egg-info
  pip install build
  python -m build
  pip install dist/frogtab-*.whl

[working-directory: "local/package/frogtab/local_server/templates"]
_package-stage: _package-static _package-templates-empty
  mv ../static/index.html ../static/icon-*.html ../static/help.html .
  sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{{{ server_base }}\"/' index.html icon-*.html help.html
  sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
  rm *.backup

_package-static:
  rm -rf local/package/frogtab/local_server/static
  cp -r app local/package/frogtab/local_server/static

[working-directory: "local/package/frogtab/local_server"]
_package-templates-empty:
  rm -rf templates
  mkdir templates

# 2️⃣  Upload the package
[working-directory: "local"]
package-upload:
  #!/bin/sh
  . .venv/bin/activate
  pip install twine
  twine upload package/dist/*

# 3️⃣  Pack a snap
[working-directory: "local/snapcraft"]
snap:
  snapcraft pack

# 4️⃣  Upload a snap to the candidate channel
[working-directory: "local/snapcraft"]
snap-upload version:
  snapcraft upload --release=candidate frogtab_{{version}}_amd64.snap

# Check and format code
[working-directory: "local"]
ruff:
  ruff check
  ruff format

# Update LICENSE files
licenses:
  wget -O LICENSE_openpgp "https://raw.githubusercontent.com/openpgpjs/openpgpjs/main/LICENSE"
  cp LICENSE_openpgp local/package

# Update libs and file hashes
app: _app-libs
  scripts/update_hashes.py

[working-directory: "app"]
_app-libs:
  wget -O simple.min.css "https://cdn.simplecss.org/simple.min.css"
  wget -O openpgp.min.mjs "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs"
