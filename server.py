from datetime import datetime
from socket import socket
from threading import Thread
from urllib import request
from json import loads, dumps, JSONDecodeError
from os import system, name
import sys
import pychat_ui


class Server:
    connections_list = []

    def clear_screen(self,):
        system('cls' if name == 'nt' else 'clear')

    def get_time(self,):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S ')
        return current_time

    def save_log(self, data, open_type,):
        log_file = open('log.txt', open_type)
        log_file.write(data)
        log_file.close()

    def save_config(self, max_connections, port, enable_log, enable_ui,):
        parameters_list = [{'max_connections': max_connections}, {'port': port}, {'enable_log': enable_log}, {'enable_ui': enable_ui}]
        config = open('config.json', 'w')
        parametersJSON = dumps(parameters_list)
        config.write(parametersJSON)

    def accept_new_clients(self, connections_list, max_connections):
        while True:
            if len(connections_list) < max_connections:
                self.connection, self.address = self.sock.accept()
                self.connections_list.append(self.connection)
                time = self.get_time()
                print(f'{self.get_time()} {self.address[0]} connected!')
                new_user_msg = self.serialize_data(self.get_time(), 'connected!', self.address[0])
                self.send_messages(new_user_msg)
                get_msg = Thread(target=self.get_data, args=(self.connection, self.address[0]))
                get_msg.start()
            else:
                self.connection, self.address = self.sock.accept()
                full_server_error = self.serialize_data(self.get_time(), 'Server is full!', 'Server:')
                self.connection.sendall(bytes(dumps(full_server_error)))

    def configure(self,):
        while True:
            print('Would you like to configure server now? [Y/n]')
            answer = input('> ').lower().strip()
            if answer == 'y':
                try:
                    self.clear_screen()
                    max_connections_input = int(input('Enter value for limit of connections > ').strip())
                    port_input = int(input('Enter port > ').strip())

                    enable_log_input = input('Enable log? (Y/n) > ').lower().strip()
                    if enable_log_input =='y':
                        enable_log_input = True
                    elif enable_log_input == 'n':
                        enable_log_input = False
                    else:
                        raise ValueError

                    enable_ui_input = input('Enable UI symbols? (Y/n) > ').lower().strip()
                    if enable_ui_input == 'y':
                        enable_ui_input = True
                    elif enable_ui_input == 'n':
                        enable_ui_input = False
                    else:
                        raise ValueError

                    save_config_input = input('Save current settings to new configuration file? (Y/n) > ').lower().strip()
                    if save_config_input == 'y':
                        self.save_config(max_connections_input, port_input, enable_log_input, enable_ui_input)
                    elif save_config_input == 'n':
                        pass
                    else:
                        raise ValueError
                    self.clear_screen()
                except ValueError:
                    self.clear_screen()
                    print('[ERROR] Error in data entry!')
                else:
                    return max_connections_input, port_input, enable_log_input, enable_ui_input
            elif answer == 'n':
                self.clear_screen()
                print('Using standart variables...')
                return 5, 8000, False, False
            else:
                self.clear_screen()
                print('[ERROR] Unknown command!')

    def get_data(self, conn, address):
        while True:
            try:
                data = conn.recv(2048).decode('utf-8')
                if data:
                    data_dict = loads(data)
                    data = f'{data_dict["sending_time"]} {address} - {data_dict["message"]}'
                    print(data)
                    # conn.send(bytes(encoding='utf-8')) # Respond to client that server got message
                    send_data = self.serialize_data(data_dict['sending_time'], data_dict['message'], address)
                    self.send_messages(send_data)
            except (ConnectionResetError, ConnectionAbortedError):
            	conn.close()
            	self.connections_list.remove(conn)
            	print(f'{self.get_time()} {self.address[0]} disconnected!')
            	connection_aborted_msg = self.serialize_data(self.get_time(), 'disconnected!', self.address[0])
            	self.send_messages(connection_aborted_msg)
            	break
    
    def serialize_data(self, sending_time, message, address):
    	message_dict = {
    		'sending_time': sending_time,
    		'message': message,
    		'sender_address': address,
    		}
    	serialized_dict = dumps(message_dict)
    	return serialized_dict


    def send_messages(self, message):
        if enable_log:
            self.save_log(message, 'a')
        for user in self.connections_list:
            message = dumps(message)
            user.sendall(bytes(message, encoding='utf-8'))

    def run_server(self, max_connections, port,):
        self.sock = socket()
        self.sock.bind(("", port))
        self.sock.listen(max_connections)
        external_ip = request.urlopen('http://ident.me').read().decode('utf-8')
        start_time = server.get_time()
        return external_ip, start_time


if __name__ == '__main__':
    server = Server()
    
    try:
        config = open('config.json').read()
        config = loads(config)
    except FileNotFoundError:
        print('[ERROR] Configuration file not found!')
        max_connections, port, enable_log, enable_ui = server.configure()
    except JSONDecodeError:
        print('[ERROR] JSON decoding error!')
        max_connections, port, enable_log, enable_ui = server.configure()
    else:
        try:
            max_connections = config[0]['max_connections']
            port = config[1]['port']
            enable_log = config[2]['enable_log']
            enable_log = bool(enable_log)
            enable_ui = config[3]['enable_ui']
            enable_ui = bool(enable_ui)
        except ValueError:
            print('[ERROR] Error in config file!')
            max_connections, port, enable_log, enable_ui = server.configure()

    logo = pychat_ui.logo.get_logo('server') if enable_ui else pychat_ui.logo.get_raw_logo('server')
    print(logo)

    license = pychat_ui.license.get_license() if enable_ui else pychat_ui.license.get_raw_license()
    print(license)

    external_ip, start_time = server.run_server(max_connections, port)

    if enable_ui:
        info_table = pychat_ui.server_infotable.get_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        raw_info_table = pychat_ui.server_infotable.get_raw_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        if enable_log:
            server.save_log(raw_info_table, 'w')
    else:
        info_table = pychat_ui.server_infotable.get_raw_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        if enable_log:
            server.save_log(info_table, 'w')
    print(info_table)

    connection = Thread(target=server.accept_new_clients, args=(server.connections_list, max_connections,))
    connection.start()
