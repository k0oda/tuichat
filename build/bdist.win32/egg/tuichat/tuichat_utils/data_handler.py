from os import system, name
from datetime import datetime
from json import dumps


class Server():
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
            if output =='y':
                output = True
            elif output == 'n':
                output = False
            else:
                raise ValueError
        elif type == 'enable_ui':
            output = input('Enable UI symbols? (Y/n) > ').lower().strip()
            if output == 'y':
                output = True
            elif output == 'n':
                output = False
            else:
                raise ValueError
        return output


class Client():
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
