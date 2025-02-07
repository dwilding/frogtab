import sys

from .version import __version__
from .cli_commands import Commands

def main():
    args = sys.argv[1:]
    if args == ['--version'] or args == ['-V']:
        print(f'Frogtab Local {__version__}')
        return
    if args == ['help'] or args == ['--help'] or args == ['-h']:
        print_help()
        return
    commands = Commands()
    if not args:
        commands.send()
        return
    if args == ['start']:
        commands.start()
        return
    if args == ['stop']:
        commands.stop()
        return
    if args == ['status']:
        commands.status()
        return
    if len(args) == 2 and args[0] == 'get':
        if args[1] == 'port':
            commands.get_port()
            return
        if args[1] == 'backup-file':
            commands.get_backup_file()
            return
        if args[1] == 'registration-server':
            commands.get_registration_server()
            return
    if len(args) == 3 and args[0] == 'set':
        if args[1] == 'port':
            try:
                port = int(args[2])
            except ValueError:
                print('Port must be an integer')
                sys.exit(2)
            if port < 1024:
                print('Port must be at least 1024')
                sys.exit(2)
            commands.set_port(port)
            return
        if args[1] == 'backup-file':
            commands.set_backup_file(str(args[2]))
            return
        if args[1] == 'registration-server':
            commands.set_registration_server(str(args[2]))
            return
    print('For a summary of how to use \'frogtab\', run \'frogtab help\'')
    sys.exit(2)


def print_help():
    print("""Frogtab Local enables you to run the Frogtab task manager on localhost.
Use 'frogtab' to manage Frogtab Local and send tasks to Frogtab.

Usage:
  frogtab         Send a task to Frogtab
                  (starting Frogtab Local if it isn't running)
  frogtab start   Start Frogtab Local
  frogtab stop    Stop Frogtab Local
  frogtab status  Check whether Frogtab Local is running

Change/display config:
  frogtab set <setting> <value>
  frogtab get <setting>

<setting> is one of:
  port                 Port that Frogtab Local runs on
                       (default: 5000)
  backup-file          Location of the automatic backup of your Frogtab data
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
  NO_COLOR=1           If set, 'frogtab' doesn't display any colored text.""")


if __name__ == '__main__':
    main()