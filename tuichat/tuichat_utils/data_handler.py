from .exceptions import InputTypeError
from os import system, name
from datetime import datetime
from json import dumps


class Server:
    def serialize_server_data(message, address, uuid, type):
        message_dict = {
            'message': message,
            'sender_address': address,
            'type': type
            }
        serialized_dict = dumps(message_dict) + uuid
        return serialized_dict

    def configuration_input(type,):
        if type == 'max_connections':
            output = int(input('Enter value for limit of connections > ').strip())
            if output <= 0:
                raise ValueError
        elif type == 'port':
            output = int(input('Enter port > ').strip())
            if output < 0:
                raise ValueError
        elif type == 'enable_log':
            output = input('Enable log? (Y/n) > ').lower().strip()
            output = True if output == 'y' else False
        elif type == 'enable_ui':
            output = input('Enable UI symbols? (Y/n) > ').lower().strip()
            output = True if output == 'y' else False
        else:
            raise InputTypeError('No input type chosen')
        return output

    def save_log(data, open_type,):
        log_file = open('log.txt', open_type)
        log_file.write(data)
        log_file.close()

    def save_config(max_connections, port, enable_log, enable_ui,):
        parameters_list = [{'max_connections': max_connections}, {'port': port}, {'enable_log': enable_log}, {'enable_ui': enable_ui}]
        config = open('config.json', 'w')
        parameters_json = dumps(parameters_list)
        config.write(parameters_json)


class Client:
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

    def serialize_client_data(message, uuid, type):
        message_dict = {
            'message': message,
            'type': type
            }
        serialized_dict = dumps(message_dict) + uuid
        return serialized_dict


def clear_screen():
    system('cls' if name == 'nt' else 'clear')


def get_time():
    current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S ')
    return current_time
