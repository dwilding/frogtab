from pathlib import Path
import sys

from ._version import __version__
from ._exceptions import (
    ReadError,
    WriteError,
    WrongVersionError,
    WrongAppError,
    RunningError,
    NotRunningError
)
from . import _client
from . import _env

def main():
    args = sys.argv[1:]
    if args == ["--version"] or args == ["-V"]:
        print(f"Frogtab Local {__version__}", end=_env.end())
        return
    if args == ["help"] or args == ["--help"] or args == ["-h"]:
        print_help()
        return
    if args == ["help", "--snap"]:
        print_help(True)
        return
    try:
        run_command(args)
    except (ReadError, WriteError) as e:
        print(f"{_env.error()} {e}")
        sys.exit(13)
    except (WrongVersionError, WrongAppError) as e:
        print(f"{_env.error()} {e}")
        sys.exit(1)

def run_command(args):
    if not args:
        send()
        return
    if args == ["start"]:
        start()
        return
    if args == ["stop"]:
        stop()
        return
    if args == ["status"]:
        status()
        return
    if args == ["find-backup"]:
        backup_file = _client.get_backup_file(_env.config_path())
        print(Path(backup_file).absolute(), end=_env.end())
        return
    if len(args) == 2 and args[0] == "get":
        if args[1] == "port":
            print(_client.get_port(_env.config_path()), end=_env.end())
            return
        if args[1] == "expose":
            print(_yesno(_client.get_expose(_env.config_path())), end=_env.end())
            return
        if args[1] == "backup-file":
            print(_client.get_backup_file(_env.config_path()), end=_env.end())
            return
        if args[1] == "registration-server":
            print(_client.get_registration_server(_env.config_path()), end=_env.end())
            return
    if len(args) == 3 and args[0] == "set":
        if args[1] == "port":
            try:
                port = int(args[2])
            except ValueError:
                print(f"{_env.error()} port must be an integer")
                sys.exit(2)
            if port < 1024:
                print(f"{_env.error()} port must be at least 1024")
                sys.exit(2)
            set_port(port)
            return
        if args[1] == "expose":
            try:
                expose = _bool(args[2])
            except KeyError:
                print(f"{_env.error()} exposure setting must be 'yes' or 'no'")
                sys.exit(2)
            set_expose(expose)
            return
        if args[1] == "backup-file":
            set_backup_file(args[2])
            return
        if args[1] == "registration-server":
            set_registration_server(args[2])
            return
    print("For a summary of how to use 'frogtab', run 'frogtab help'")
    sys.exit(2)

def send():
    config_path = _env.config_path()
    _env.check_ports_file()
    backup_path = Path(_client.get_backup_file(config_path))
    if backup_path.is_dir():
        print(f"{_env.error()} '{backup_path.absolute()}' is a directory")
        sys.exit(1)
    port = _client.get_port(config_path)
    started = _client.start(config_path)
    task = _env.task_or_exit()
    try:
        _client.send(port, task)
    except NotRunningError:
        print(f"{_env.error()} Frogtab Local is not running on port {port}")
        _env.log_not_running(port)
        sys.exit(1)
    if started:
        print(f"{_env.tick()} Started Frogtab Local and sent task to Frogtab")
        print(f"To access Frogtab, open {_env.url(port)} in your browser")
    else:
        print(f"{_env.tick()} Sent task to Frogtab")
    _env.log_running(port)

def start():
    config_path = _env.config_path()
    _env.check_ports_file()
    backup_path = Path(_client.get_backup_file(config_path))
    if backup_path.is_dir():
        print(f"{_env.error()} '{backup_path.absolute()}' is a directory")
        sys.exit(1)
    port = _client.get_port(config_path)
    if _client.start(config_path):
        print(f"{_env.tick()} Started Frogtab Local")
        print(f"To access Frogtab, open {_env.url(port)} in your browser")
    else:
        print(f"Frogtab Local is running on port {port}")
    _env.log_running(port)

def stop():
    config_path = _env.config_path()
    _env.check_ports_file()
    port = _client.get_port(config_path)
    if _client.stop(port):
        print(f"{_env.tick()} Stopped Frogtab Local")
    else:
        print(f"Frogtab Local is not running on port {port}")
    _env.log_not_running(port)

def status():
    config_path = _env.config_path()
    _env.check_ports_file()
    port = _client.get_port(config_path)
    if not _client.is_running(port):
        print(f"Frogtab Local is not running on port {port}")
        _env.log_not_running(port)
        sys.exit(1)
    print(f"Frogtab Local is running on port {port}")
    _env.log_running(port)

def set_port(new_port: int) -> None:
    config_path = _env.config_path()
    port = _client.get_port(config_path)
    if port == new_port:
        print(f"Frogtab Local is already set to use port {port}")
        return
    try:
        _client.set_port(config_path, new_port)
    except RunningError as e:
        print(f"{_env.error()} {e}")
        print("Stop Frogtab Local before changing the port")
        sys.exit(1)
    print(f"{_env.tick()} Changed port from {port} to {new_port}")

def set_expose(new_expose: bool) -> None:
    config_path = _env.config_path()
    expose = _client.get_expose(config_path)
    if expose == new_expose:
        if expose:
            print(f"Frogtab Local is already set to expose")
        else:
            print(f"Frogtab Local is already set to not expose")
        return
    try:
        _client.set_expose(config_path, new_expose)
    except RunningError as e:
        print(f"{_env.error()} {e}")
        print("Stop Frogtab Local before changing the exposure setting")
        sys.exit(1)
    print(f"{_env.tick()} Changed exposure setting from '{_yesno(expose)}' to '{_yesno(new_expose)}'")

def set_backup_file(new_backup_file: str) -> None:
    config_path = _env.config_path()
    backup_file = _client.get_backup_file(config_path)
    if backup_file == new_backup_file:
        print(f"Frogtab Local is already set to use backup file '{backup_file}'")
        return
    try:
        _client.set_backup_file(config_path, new_backup_file)
    except RunningError as e:
        print(f"{_env.error()} {e}")
        print("Stop Frogtab Local before changing the backup file")
        sys.exit(1)
    print(f"{_env.tick()} Changed backup file from '{backup_file}' to '{new_backup_file}'")

def set_registration_server(new_registration_server: str) -> None:
    config_path = _env.config_path()
    registration_server = _client.get_registration_server(config_path)
    if registration_server == new_registration_server:
        print(f"Frogtab Local is already set to use registration server '{registration_server}'")
        return
    try:
        _client.set_registration_server(config_path, new_registration_server)
    except RunningError as e:
        print(f"{_env.error()} {e}")
        print("Stop Frogtab Local before changing the registration server")
        sys.exit(1)
    print(f"{_env.tick()} Changed registration server from '{registration_server}' to '{new_registration_server}'")

def _yesno(value: bool) -> str:
    return {
        True: "yes",
        False: "no"
    }[value]

def _bool(value: str) -> str:
    return {
        "yes": True,
        "no": False
    }[value]


def print_help(snap: bool = False):
    help_working_dir = "the working directory"
    help_ports_file = """
  FROGTAB_PORTS_FILE   If set, specifies where Frogtab Local writes a list of
                       ports that Frogtab Local is running on."""
    if snap:
        help_working_dir = _env.snap_working_dir()
        help_ports_file = ""
    print(f"""Frogtab Local enables you to run the Frogtab task manager on localhost.
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
                       (default: Frogtab_backup.json in {help_working_dir})
  registration-server  Server that Frogtab uses if you register this device
                       (default: https://frogtab.com/)

Additional commands:
  frogtab help         Display a summary of how to use 'frogtab'
  frogtab --version    Display the version of Frogtab Local that is installed

Environment variables:
  FROGTAB_CONFIG_FILE  If set, specifies where Frogtab Local stores settings
                       and internal state. If not set, Frogtab Local uses
                       Frogtab_config.json in {help_working_dir}.{help_ports_file}
  NO_COLOR=1           If set, 'frogtab' doesn't display any colored text.""")


if __name__ == "__main__":
    main()