# Frogtab Local

Frogtab Local is a version of https://frogtab.com that you can run on your computer.
Frogtab Local is implemented as a Flask app that runs in development mode.
You're encouraged to tinker with the app!

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
    This approach improves support for automatic backups.

    Plus, this approach lets you customize how the Flask app saves backup files.
    See "Adding your own backup method" below.

  - You can register for a personal link without sharing your experience of using Frogtab Local.

    > **NOTE:** If you register for a personal link, Frogtab Local tries to register with frogtab.com.
    > Frogtab Local does not include a self-hostable registration server.

  - You can customize the placeholder text of your personal link.
    This is actually possible with frogtab.com too, but you have to manually adjust the URL of your personal link.
    With Frogtab Local, you can use the `data-vibe` attribute at the top of *static/help.html* to customize the placeholder text.

## Adding your own backup method

Define your backup method as a function in *config.py* and apply the `@backup` decorator to the function. For example:

```py
@backup('Save to Desktop')
def save_to_desktop(data):
    write_json('/home/dave/Desktop/Frogtab_backup.json', data)
```

The `data` parameter is a dictionary that contains the backup data from your browser.
The argument to `@backup` is the name of the backup method that will appear on the Help page.

## License

Frogtab Local is licensed under the MIT License.
For details, see *LICENSE*.

Frogtab Local uses OpenPGP.js for PGP encryption and decryption.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see *LICENSE_openpgp*.
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.