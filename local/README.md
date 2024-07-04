# Frogtab Local

Frogtab Local is a version of https://frogtab.com that you can run on your computer.
Frogtab Local is implemented as a Flask app that runs in development mode.
You're encouraged to tinker with the app!

Frogtab Local supports personal links, but your device will be registered with frogtab.com.
If you self-host Frogtab, you can configure Frogtab Local to use your own server instead.
See below for details.

## Requirements

  - Python 3.8 or later. See https://www.python.org/downloads/
  - Flask. See https://flask.palletsprojects.com/en/3.0.x/installation/

## Running the Flask app

Open a terminal in the directory that contains *app.py*, then use the following command:
    
```sh
flask run
```

The Flask app starts:

```
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

To access Frogtab Local, open http://127.0.0.1:5000 in your browser.

To specify a different port, use the following command instead of `flask run`:

```sh
flask run --port 8080
```

## Differences between Frogtab Local and frogtab.com

  - Frogtab Local doesn't rely on your browser to save backup files.
    Instead, the Flask app can save backup files.
    This approach improves support for automatic backups and lets you add your own backup methods. See below for details.

  - You can register for a personal link without sending a comment.

  - You can customize the placeholder text of your personal link.
    This is actually possible with frogtab.com too, but you have to manually adjust the URL of your personal link.
    With Frogtab Local, you can use the `data-vibe` attribute at the top of *static/help.html* to customize the placeholder text.

## Adding your own backup method

Define your backup method as a function in *config.py* and apply the `@backup` decorator to the function. For example:

```py
@backup('Save to Desktop')
def save_to_desktop(data):
    write_json(data, '/home/dave/Desktop/Frogtab_backup.json')
```

The `data` parameter is a dictionary that contains the backup data from your browser.
The argument to `@backup` is the name of the backup method that will appear on the help page of Frogtab Local.

## Using a self-hosted server for personal links

If you have installed Frogtab on your own server, you can configure Frogtab Local to use your server for personal links.
To learn how to install Frogtab on your server, see https://github.com/dwilding/frogtab#self-hosting-frogtab.

After installing Frogtab on your server, modify the `data-server-base` attribute at the top of the following files:

  - *static/index.html*
  - *static/icon-normal.html*
  - *static/icon-notify.html*
  - *static/help.html*

In the `data-server-base` attribute, replace `https://frogtab.com/` by the URL of your installation of Frogtab.

## License
Frogtab Local is licensed under the MIT License.
For details, see *LICENSE*.

Frogtab Local uses OpenPGP.js for PGP encryption and decryption.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see *LICENSE_openpgp*.
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.