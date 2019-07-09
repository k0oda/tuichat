#!/usr/bin/env python3

from uuid import UUID
from socket import socket, timeout, gaierror
from tuichat import tuichat_utils
from threading import Timer
from json import loads
from tqdm import tqdm
from time import sleep


class Client:
    def __init__(self,):
        self.data_queue = []
        self.freeze = False
        self.msg_timeout = 0.1
        self.msg_max_symbols = 300

    def main(self,):
        logo_obj = tuichat_utils.ui.Logo('client')
        logo = logo_obj.logo
        print(logo)

        license_obj = tuichat_utils.ui.License()
        copyright = license_obj.license
        print(copyright)

        host, port = self.connect()
        tuichat_utils.data_handler.clear_screen()
        print(logo)
        print(copyright)

        connection_info_obj = tuichat_utils.ui.ConnectionInfo(host, port)
        connection_info = connection_info_obj.connection_info
        print(connection_info)

        self.start_client()

    def receive_data(self,):
        if not self.freeze:
            try:
                data = self.sock.recv(1128).decode('utf-8')
                data = data.split(self.uuid)
                data = data[:-1]
                for element in data:
                    data_dict = loads(element)
                    if data_dict['type'] == 'server_closed':
                        raise ConnectionResetError
                    else:
                        self.data_queue.append(f'{tuichat_utils.data_handler.get_time()} {data_dict["sender_address"]} - {data_dict["message"]}')
            except timeout:
                return
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                self.handle_server_closed()

    def print_data(self,):
        for data in self.data_queue:
            print(data)
        self.data_queue.clear()

    def send_data(self,):
        while not self.freeze:
            try:
                self.receive_data()
                Timer(1.0, self.receive_data).start()
                if self.data_queue:
                    prompt = f'You have [{len(self.data_queue)}] messages. Enter a message or enter "/r" to print new messages > '
                else:
                    prompt = 'Enter a message > '
                message_input = input(prompt)
                if len(message_input) > self.msg_max_symbols:
                    print(f'║ The number of symbols of your message is more than {self.msg_max_symbols}, using first {self.msg_max_symbols} symbols')
                    message_input = message_input[:self.msg_max_symbols]
                if message_input != "/r":
                    message = tuichat_utils.data_handler.Client.serialize_client_data(message_input, self.uuid, 'message')
                    self.sock.sendall(bytes(message, encoding="utf-8"))
                else:
                    self.print_data()
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                self.handle_server_closed()

    def start_client(self,):
        try:
            self.send_data()
        except (KeyboardInterrupt, SystemExit):
            self.disconnect()
        except Exception as ex:
            print(ex)
            self.disconnect()

    def handle_server_closed(self,):
        print("\n║ Server closed!")
        self.freeze = True
        connect_again = tuichat_utils.data_handler.Client.connect_input('reconnect')
        if connect_again:
            respond = self.reconnect()
            if respond is True:
                print("║ Connection established!\n")
                self.freeze = False
                self.start_client()
            else:
                print("\n║ Server did not respond!")
                input("Press any key to exit...")
                exit()
        else:
            exit()

    def reconnect(self,):
        i = 0
        pbar = tqdm(total=5)
        while i <= 5:
            try:
                self.sock.close()
                self.sock = socket()
                self.sock.connect((self.host, self.port))
            except Exception as ex:
                print(f'An error occured: {ex}')
                sleep(1)
                i += 1
                pbar.update(1)
                continue
            else:
                self.setup_connection()
                pbar.close()
                return True
        else:
            pbar.close()
            return False

    def receive_uuid(self,):
        uuid_bytes = self.sock.recv(16)
        self.uuid = str(UUID(bytes=uuid_bytes))

    def setup_connection(self,):
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        self.receive_uuid()
        self.sock.settimeout(self.msg_timeout)

    def connect(self, success_connect=False,):
        self.sock = socket()

        while not success_connect:
            try:
                self.host = tuichat_utils.data_handler.Client.connect_input('host')
                self.port = tuichat_utils.data_handler.Client.connect_input('port')
                self.sock.connect((self.host, self.port))
                self.setup_connection()
            except KeyboardInterrupt:
                exit()
                break
            except gaierror:
                print("║ Host not found!\n")
            except (ConnectionRefusedError, timeout, TimeoutError):
                print("║ Host rejected connection request!\n")
            except ValueError as ex:
                print(f"║ ValueError: {ex}!\n")
            else:
                success_connect = True
        return self.host, self.port

    def disconnect(self,):
        print(f'\nDisconnecting from {self.sock.getsockname()[0]} ...')
        try:
            self.freeze = True
            message = tuichat_utils.data_handler.Client.serialize_client_data('', self.uuid, 'disconnect')
            self.sock.sendall(bytes(message, encoding="utf-8"))
            self.sock.close()
        except Exception as ex:
            print(ex)
        else:
            print('Successfully disconnected from server! [OK]')
            answer = tuichat_utils.data_handler.Client.connect_input('disconnect')
            if answer:
                self.connect()
            else:
                exit()


if __name__ == '__main__':
    client = Client()
    client.main()
