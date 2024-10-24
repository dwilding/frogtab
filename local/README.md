# Frogtab Local

Frogtab Local is a version of https://frogtab.com that you can run on your computer.
Frogtab Local is implemented as a Flask app that runs in development mode.
I encourage you to tinker with the app!

Frogtab Local supports personal links, but your device will be registered with frogtab.com.
If you self-host Frogtab, you can configure Frogtab Local to use your own server instead.
See below for details.

## Requirements

  - Python 3.8 or later. See https://www.python.org/downloads/
  - Flask.
    I recommend that you install Flask in a virtual environment.
    See https://flask.palletsprojects.com/en/3.0.x/installation/#virtual-environments

## Running the Flask app

Open a terminal in the directory that contains *app.py*, then enter the following command:
    
```
python3 app.py
```

The Flask app starts:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

To access Frogtab, open http://127.0.0.1:5000 in your browser.

To specify a different port, modify the `local_port` variable in *config.py*, then run `python app.py` again.

## Adding your own backup method

Frogtab Local doesn't rely on your browser to save backup files.
Instead, the Flask app can save backup files.
This approach improves support for automatic backups and lets you add your own backup methods.

To add your own backup method, define your backup method as a function in *config.py* and apply the `@backup` decorator to the function.
For example:

```py
@backup('Save to Desktop')
def save_to_desktop(data):
    write_json(data, '/home/dave/Desktop/Frogtab_backup.json')
```

The `data` parameter is a dictionary that contains the backup data from your browser.
The argument to `@backup` is the name of the backup method that will appear in the list of backup methods.

## Using a self-hosted server for personal links

If you have installed Frogtab on your own server, you can configure Frogtab Local to use your server for personal links.
To learn how to install Frogtab on your server, see https://github.com/dwilding/frogtab#self-hosting-frogtab.

After installing Frogtab on your server, set the `registration_server` variable in *config.py* to the URL of your installation of Frogtab.

## License

Frogtab Local is licensed under the MIT License.
For details, see *LICENSE*.

Frogtab Local uses OpenPGP.js for PGP encryption.
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see *LICENSE_openpgp*.