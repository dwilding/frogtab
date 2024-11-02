# Frogtab Local

Frogtab Local is a version of https://frogtab.com that you can run on your computer.
Frogtab Local is implemented as a Flask app that runs in development mode.
I encourage you to tinker with the app!

Frogtab Local supports personal links, but your device will be registered with frogtab.com.
If you self-host Frogtab, you can configure Frogtab Local to use your own server instead.
See *config.py* for details.

## Installing the Flask app

These instructions explain how to install the Flask app from source.
If you use Linux, it's easier to install Frogtab Local from the Snap Store.
See https://snapcraft.io/frogtab.

You'll need Python 3.8 or later. See https://www.python.org/downloads/.

To install the Flask app, open a terminal in the directory that contains *app.py*,
then enter the following commands:

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Running the Flask app

To run the Flask app, use `python app.py`.

The Flask app starts:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

To access Frogtab, open http://127.0.0.1:5000 in your browser.

To specify a different port, modify the `local_port` variable in *config.py*, then run `python app.py` again.

## License

Frogtab Local is licensed under the MIT License.
For details, see *LICENSE*.

Frogtab Local uses OpenPGP.js for PGP encryption.
The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs.
OpenPGP.js is licensed under the GNU Lesser General Public License.
For details, see *LICENSE_openpgp*.