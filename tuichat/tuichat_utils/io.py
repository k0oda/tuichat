from .exceptions import InputTypeError


class Client:
    class CLI:
        @staticmethod
        def connect_input(type,):
            if type == 'host':
                output = input('║ Enter host: ').strip()
            elif type == 'port':
                output = int(input('║ Enter port: ').strip())
            elif type == 'reconnect':
                output = input("Try to connect again? (Y/n) > ").lower().strip()
                output = True if output == 'y' else False
            elif type == 'disconnect':
                output = input('Connect to another server? (Y/n) > ').lower().strip()
                output = True if output == 'y' else False
            else:
                raise InputTypeError('No input type chosen')
            return output

        @staticmethod
        def output(data, type='msg'):
            if type.lower() != 'error':
                try:
                    print(data)
                except Exception as ex:
                    print(f'ERROR: {ex}')
            else:
                print(f'ERROR: {data}')

        @staticmethod
        def exit():
            input("Press any key to exit...")
            exit()

    class GUI:
        @staticmethod
        def connect_input(type,):
            return
