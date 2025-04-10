# Frogtab Local

Frogtab Local is a version of [frogtab.com](https://frogtab.com) that you can run on your computer. With Frogab Local, you can:

  - Use Frogtab offline
  - Automatically back up your data in any browser
  - Send tasks to Frogtab via a terminal

Frogtab Local supports personal links, but your device will be registered with frogtab.com. If you self-host Frogtab, you can configure Frogtab Local to use your own server instead.

In this README:

  - [Installing Frogtab Local](#installing-frogtab-local)
  - [Starting Frogtab Local](#starting-frogtab-local)
  - [Sending tasks to Frogtab](#sending-tasks-to-frogtab)
  - [Command reference](#command-reference)
  - [Python reference](#python-reference)

## Installing Frogtab Local

These instructions explain how to install Frogtab Local as a Python package in a virtual environment. You'll need Python 3.8 or later. See [Download Python](https://www.python.org/downloads/).

If you use Linux, I recommend that you install the [Frogtab Local snap](https://snapcraft.io/frogtab) instead.

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

If you see the error "a different app is using port 5000", you'll need to use a different port. In this case, run the following commands:

```
frogtab set port 5001  # For example
frogtab start
```

As you use Frogtab, your data is automatically backed up by Frogtab Local. The default location of the backup file is *Frogtab_backup.json* in the working directory. You can use `frogtab set backup-file` to change the location of the backup file. To learn more, run `frogtab help` or see [Command reference](#command-reference).

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

Display/change settings:
  frogtab get <setting>
  frogtab set <setting> <value>

Available settings:
  port                 Port that Frogtab Local runs on
                       (default: 5000)
  expose yes/no        Allow access to Frogtab Local on all network interfaces
                       (default: no)
  backup-file          Location of the Frogtab backup file
                       (default: Frogtab_backup.json in the working directory)
  registration-server  Server that Frogtab uses if you register this device
                       (default: https://frogtab.com/)

Additional commands:
  frogtab help         Display a summary of how to use 'frogtab'
  frogtab --version    Display the version of Frogtab Local that is installed

Environment variables:
  FROGTAB_CONFIG_FILE  If set, specifies where Frogtab Local stores settings
                       and internal state. If not set, Frogtab Local uses
                       Frogtab_config.json in the working directory.
  FROGTAB_PORTS_FILE   If set, specifies where Frogtab Local writes a list of
                       ports that Frogtab Local is running on.
  NO_COLOR=1           If set, 'frogtab' doesn't display any colored text.
```

## Python reference

TODO: https://github.com/dwilding/frogtab/issues/8
