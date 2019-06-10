#!/usr/bin/env python3

from pychat_utils import ui, data_handler
from socket import socket
from threading import Thread
from urllib import request
from json import loads, dumps, JSONDecodeError
from uuid import uuid4


class Server:
    connections_list = []
    uuid = str(uuid4())

    def main(self,):
        self.get_settings()

        logo_obj = ui.Logo('server')
        logo = logo_obj.logo if self.enable_ui else logo_obj.raw_logo
        print(logo)

        license_obj = ui.License()
        copyright = license_obj.license if self.enable_ui else license_obj.raw_license
        print(copyright)

        external_ip, start_time = self.run_server()

        server_infotable_obj = ui.ServerInfotable(start_time, self.port, self.max_connections, external_ip, self.enable_log, self.enable_ui)
        raw_infotable = server_infotable_obj.raw_infotable
        infotable = server_infotable_obj.infotable if self.enable_ui else raw_infotable
        if self.enable_log:
            server.save_log(raw_infotable, 'a')
        print(infotable)

        connection = Thread(target=self.accept_new_clients)
        connection.start()

    def get_settings(self,):
        try:
            config = open('config.json').read()
            config = loads(config)
            self.max_connections = config[0]['max_connections']
            if self.max_connections <= 0:
                raise ValueError
            self.port = config[1]['port']
            self.enable_log = config[2]['enable_log']
            self.enable_log = bool(self.enable_log)
            self.enable_ui = config[3]['enable_ui']
            self.enable_ui = bool(self.enable_ui)
        except FileNotFoundError:
            print('[ERROR] Configuration file not found!')
            self.max_connections, self.port, self.enable_log, self.enable_ui = self.configure()
        except JSONDecodeError:
            print('[ERROR] JSON decoding error!')
            self.max_connections, self.port, self.enable_log, self.enable_ui = self.configure()
        except (ValueError, KeyError):
            print('[ERROR] Error in config file! Check variables')
            self.max_connections, self.port, self.enable_log, self.enable_ui = self.configure()

    def save_log(self, data, open_type,):
        log_file = open('log.txt', open_type)
        log_file.write(data)
        log_file.close()

    def save_config(self, max_connections, port, enable_log, enable_ui,):
        parameters_list = [{'max_connections': max_connections}, {'port': port}, {'enable_log': enable_log}, {'enable_ui': enable_ui}]
        config = open('config.json', 'w')
        parametersJSON = dumps(parameters_list)
        config.write(parametersJSON)

    def configure(self,):
        while True:
            print('Would you like to configure server now? [Y/n]')
            answer = input('> ').lower().strip()
            if answer == 'y':
                try:
                    data_handler.clear_screen()
                    max_connections_input = data_handler.Server.configuration_input('max_connections')
                    port_input = data_handler.Server.configuration_input('port')

                    enable_log_input = data_handler.Server.configuration_input('enable_log')
                    enable_ui_input = data_handler.Server.configuration_input('enable_ui')

                    save_config_input = input('Save current settings to new configuration file? (Y/n) > ').lower().strip()
                    if save_config_input == 'y':
                        self.save_config(max_connections_input, port_input, enable_log_input, enable_ui_input)
                    else:
                        pass
                    data_handler.clear_screen()
                except ValueError:
                    data_handler.clear_screen()
                    print('[ERROR] Error in data entry!')
                else:
                    return max_connections_input, port_input, enable_log_input, enable_ui_input
            elif answer == 'n':
                data_handler.clear_screen()
                print('Using standart variables...')
                return 5, 8000, False, False
            else:
                data_handler.clear_screen()
                print('[ERROR] Unknown command!')

    def accept_new_clients(self,):
        while True:
            if len(self.connections_list) < self.max_connections:
                connection, address = self.sock.accept()
                self.connections_list.append(connection)
                connection.send(bytes(dumps({'uuid': self.uuid}), encoding='utf-8'))
                print(f'{data_handler.get_time()} {address[0]} connected!')
                new_user_msg = {'message': 'connected!'}
                self.send_messages(new_user_msg, address[0])
                get_msg = Thread(target=self.get_data, args=(connection, address[0]))
                get_msg.start()
                get_msg.join()
            else:
                temp_connection, _temp_address = self.sock.accept()
                temp_connection.close()

    def get_data(self, conn, address,):
        while True:
            try:
                data = conn.recv(376).decode('utf-8')
                data = data.split(self.uuid)
                data = data[:-1]
                for element in data:
                    data_dict = loads(element)
                    data = f'{data_handler.get_time()} {address} - {data_dict["message"]}'
                    print(data)
                    self.send_messages(data_dict, address)
            except (ConnectionResetError, ConnectionAbortedError):
                conn.close()
                self.connections_list.remove(conn)
                print(f'{data_handler.get_time()} {address} disconnected!')
                connection_aborted_msg = {'message': 'disconnected!'}
                self.send_messages(connection_aborted_msg, address)
                break

    def send_messages(self, data_dict, address):
        if self.enable_log:
            message = f'{data_handler.get_time()} {address} {data_dict["message"]}\n'
            self.save_log(message, 'a')

        message = data_handler.Server.serialize_server_data(data_dict['message'], address, self.uuid)
        message_to_sender = data_handler.Server.serialize_server_data(data_dict['message'], '[You]', self.uuid)
        for client in self.connections_list:
            if client.getsockname()[0] != address:
                client.sendall(bytes(message, encoding='utf-8'))
            else:
                client.sendall(bytes(message_to_sender, encoding='utf-8'))

    def run_server(self,):
        self.sock = socket()
        self.sock.bind(("", self.port))
        self.sock.listen(self.max_connections)
        external_ip = request.urlopen('http://ifconfig.me/ip').read().decode('utf-8')
        start_time = data_handler.get_time()
        return external_ip, start_time


if __name__ == '__main__':
    server = Server()
    server.main()
