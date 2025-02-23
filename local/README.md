# Frogtab Local

Frogtab Local is a version of [frogtab.com](https://frogtab.com) that you can run on your computer. With Frogab Local, you can:

  - Use Frogtab offline
  - Enable automatic backups in any browser
  - Send tasks to Frogtab via a terminal

Frogtab Local supports personal links, but your device will be registered with frogtab.com. If you self-host Frogtab, you can configure Frogtab Local to use your own server instead.


## Installing Frogtab Local

These instructions explain how to install Frogtab Local as a Python package in a virtual environment. You'll need Python 3.8 or later. See https://www.python.org/downloads/.

If you use Linux, I recommend that you install Frogtab Local from the Snap Store instead. See https://snapcraft.io/frogtab.

To install Frogtab Local in a virtual environment, run the following commands:

```
python3 -m venv .venv
. .venv/bin/activate
pip install frogtab
```


## Starting Frogtab Local

To start Frogtab Local, run the following commands:

```
. .venv/bin/activate
frogtab start
```

Frogtab Local starts:

```
✓ Started Frogtab Local
To access Frogtab, open http://localhost:5000 in your browser
```

To change the port, run the following commands:

```
frogtab stop
frogtab set port 5001  # for example
frogtab start
```

TODO: If you opened Frogtab in your browser before changing the port, you'll need to import a backup file to pair with Frogtab Local (https://github.com/dwilding/frogtab/issues/9)


## Sending tasks to Frogtab

To send a task to Frogtab:

 1. Run the following commands:

    ```
    . .venv/bin/activate
    frogtab
    ```

 2. Type the task, then press Enter. For example:

    ```
    Add a task to your inbox:
    > Record a demo video
    ✓ Sent task to Frogtab
    ```


## Command reference

Here's the output of `frogtab help`:

```
Frogtab Local enables you to run the Frogtab task manager on localhost.
Use 'frogtab' to manage Frogtab Local and send tasks to Frogtab.

Usage:
  frogtab              Send a task to Frogtab, starting Frogtab Local if needed
  frogtab start        Start Frogtab Local
  frogtab stop         Stop Frogtab Local
  frogtab status       Check whether Frogtab Local is running
  frogtab find-backup  Display the full location of the Frogtab backup file

Display/change config:
  frogtab get <setting>
  frogtab set <setting> <value>

Available settings:
  port                 Port that Frogtab Local runs on
                       (default: 5000)
  backup-file          Location of the Frogtab backup file
                       (default: Frogtab_backup.json in the working directory)
  registration-server  Server that Frogtab uses if you register this device
                       (default: https://frogtab.com/)

Additional commands:
  frogtab help         Display a summary of how to use 'frogtab'
  frogtab --version    Display the version of Frogtab Local that is installed

Environment variables:
  FROGTAB_CONFIG_FILE  If set, specifies where Frogtab Local stores config and
                       internal state. If not set, Frogtab Local uses
                       Frogtab_config.json in the working directory.
  FROGTAB_EXPOSE=1     If set when Frogtab Local starts, Frogtab Local runs on
                       all network interfaces. This can be useful if you have
                       installed Frogtab Local in a virtual machine.
  NO_COLOR=1           If set, 'frogtab' doesn't display any colored text.
```


## Python reference

TODO: https://github.com/dwilding/frogtab/issues/8