# Frogtab Local

Frogtab Local is a version of https://frogtab.com that you can run on your computer. With Frogab Local, you can:

  - Use Frogtab offline
  - Enable automatic backups in any browser
  - Send tasks to Frogtab via a terminal

Frogtab Local supports personal links, but your device will be registered with frogtab.com. If you self-host Frogtab, you can configure Frogtab Local to use your own server instead. For details, see *config.ini*.


## Installing Frogtab Local

These instructions explain how to install Frogtab Local from source. You'll need Python 3.8 or later. See https://www.python.org/downloads/.

If you use Linux, I recommend that you install Frogtab Local from the Snap Store instead. See https://snapcraft.io/frogtab.

To install Frogtab Local from source, run the following commands:

```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```


## Starting Frogtab Local

To start Frogtab Local, run the following commands:

```
$ . .venv/bin/activate
$ python frogtab.py start
```

Frogtab Local starts:

```
✓ Started Frogtab Local
To access Frogtab, open http://127.0.0.1:5000 in your browser
```

To change the port, first run `python frogtab.py stop`. Then modify the `local_port` property in *config.ini* and run `python frogtab.py start` again.


## Sending tasks to Frogtab

To send a task to Frogtab:

 1. Run the following commands:

    ```
    $ . .venv/bin/activate
    $ python frogtab.py
    ```

 2. Type the task, then press Enter. For example:

    ```
    Add a task to your inbox:
    > Record a demo video
    ✓ Sent task to Frogtab
    ```


## Command reference

Here's the output of `python frogtab.py help`:

```
TODO
```


## License

Frogtab Local is licensed under the MIT License. For details, see *LICENSE*.

Frogtab Local uses OpenPGP.js for PGP encryption. The source code of OpenPGP.js is available at https://github.com/openpgpjs/openpgpjs. OpenPGP.js is licensed under the GNU Lesser General Public License. For details, see *LICENSE_openpgp*.