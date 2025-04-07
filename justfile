_default:
  @just --list --unsorted

# 1️⃣  Review links to branches
links:
  git grep -E "frogtab/(tree|blob)/\w+"

# 2️⃣  Build the package
[working-directory: "local"]
package: app licenses ruff _package-stage
  ./build_package.sh
  mkdir -p testing
  @echo ""
  @echo "To try the package:"
  @echo "  $ cd local"
  @echo "  $ . .venv/bin/activate"
  @echo "  $ cd testing"
  @echo "  $ frogtab ..."
  @echo ""
  @echo "To upload the package:"
  @echo "  $ cd local"
  @echo "  $ . .venv/bin/activate"
  @echo "  $ pip install twine"
  @echo "  $ twine upload package/dist/*"

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

# 3️⃣  Pack the snap
[working-directory: "local/snapcraft"]
snap:
  snapcraft pack
  @echo ""
  @echo "To upload the snap:"
  @echo "  snapcraft upload --release=candidate local/snapcraft/frogtab_<version>_amd64.snap"

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
  development/update_hashes.py

[working-directory: "app"]
_app-libs:
  wget -O simple.min.css "https://cdn.simplecss.org/simple.min.css"
  wget -O openpgp.min.mjs "https://unpkg.com/openpgp@5.x/dist/openpgp.min.mjs"
