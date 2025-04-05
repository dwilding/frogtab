_default:
  @just --list --unsorted

# Build the Python package and explain how to try it
[working-directory: "local"]
local-package: _local-templates
  ./build_package.sh
  mkdir -p testing
  @echo "# To try the package:"
  @echo "$ cd local"
  @echo "$ . .venv/bin/activate"
  @echo "$ cd testing"
  @echo "$ frogtab ..."

# Explain how to upload the Python package
local-package-upload:
  @echo "# After running 'just local-package':"
  @echo "$ cd local"
  @echo "$ . .venv/bin/activate"
  @echo "$ pip install twine"
  @echo "$ twine upload package/dist/*"

[working-directory: "local/package/frogtab/local_server/templates"]
_local-templates: _local-static _local-templates-empty
  mv ../static/index.html ../static/icon-*.html ../static/help.html .
  sed -i'.backup' 's/data-server-base=\"https:\/\/frogtab\.com\/\"/data-server-base=\"{{{{ server_base }}\"/' index.html icon-*.html help.html
  sed -i'.backup' 's/data-save=\"browser\"/data-save=\"service\"/' index.html icon-*.html help.html
  rm *.backup

[working-directory: "local/package/frogtab/local_server"]
_local-templates-empty:
  rm -rf templates
  mkdir templates

_local-static:
  rm -rf local/package/frogtab/local_server/static
  cp -r app local/package/frogtab/local_server/static

# Pack the snap and explain how to upload it
[working-directory: "local/snapcraft"]
local-snap:
  snapcraft pack
  @echo "# To upload the snap:"
  @echo "$ snapcraft upload --release=candidate local/snapcraft/frogtab_<version>_amd64.snap"
