import sys

from frogtab import Commands

def main():
    args = sys.argv[1:]
    if args == ['--version'] or args == ['-V']:
        print(f'Frogtab Local {frogtab.__version__}')
        return
    if args == ['help'] or args == ['--help'] or args == ['-h']:
        # TODO: Show help
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
    # TODO: Show usage
    sys.exit(2)

if __name__ == '__main__':
    main()