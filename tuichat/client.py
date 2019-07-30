#!/usr/bin/env python3

import rsa
from uuid import UUID
from socket import socket, timeout, gaierror
from tuichat import tuichat_utils
from threading import Timer
from json import loads
from tqdm import tqdm
from time import sleep


class Client:
    def __init__(self, mode='cli'):
        self.pubkey, self.privkey = rsa.newkeys(512)
        self.data_queue = []
        self.freeze = False
        self.msg_timeout = 0.1
        self.msg_max_symbols = 300
        self.mode = mode
        if self.mode.lower() == 'gui':
            self.io = tuichat_utils.io.Client.GUI
        else:
            self.io = tuichat_utils.io.Client.CLI

    def main(self,):
        logo_obj = tuichat_utils.ui.Logo('client')
        logo = logo_obj.logo
        self.io.output(logo)

        license_obj = tuichat_utils.ui.License()
        copyright = license_obj.license
        self.io.output(copyright)

        host, port = self.connect()
        tuichat_utils.data_handler.clear_screen()
        self.io.output(logo)
        self.io.output(copyright)

        connection_info_obj = tuichat_utils.ui.ConnectionInfo(host, port)
        connection_info = connection_info_obj.connection_info
        self.io.output(connection_info)

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
            self.io.output(data)
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
                    self.io.output(f'║ The number of symbols of your message is more than {self.msg_max_symbols}, using first {self.msg_max_symbols} symbols')
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
            self.io.output(ex, 'error')
            self.disconnect()

    def handle_server_closed(self,):
        self.io.output("\n║ Server closed!")
        self.freeze = True
        connect_again = self.io.connect_input('reconnect')
        if connect_again:
            respond = self.reconnect()
            if respond is True:
                self.io.output("║ Connection established!\n")
                self.freeze = False
                self.start_client()
            else:
                self.io.output("\n║ Server did not respond!")
                self.io.exit()
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
                self.io.output(ex, 'error')
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

    def receive_key(self,):
        pub = self.sock.recv(172).decode('utf-8')
        self.server_pub = pub

    def send_key(self,):
        self.sock.send(bytes(str(self.pubkey), encoding='utf-8'))

    def setup_connection(self,):
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        self.receive_uuid()
        self.receive_key()
        self.send_key()
        self.sock.settimeout(self.msg_timeout)

    def connect(self, success_connect=False, host=None, port=None):
        self.sock = socket()

        while not success_connect:
            try:
                if self.mode == 'cli':
                    self.host = self.io.connect_input('host')
                    self.port = self.io.connect_input('port')
                else:
                    self.host = host
                    self.port = port
                self.sock.connect((self.host, self.port))
                self.setup_connection()
            except KeyboardInterrupt:
                exit()
                break
            except gaierror:
                self.io.output("║ Host not found!\n", 'error')
            except (ConnectionRefusedError, timeout, TimeoutError):
                self.io.output("║ Host rejected connection request!\n", 'error')
            except ValueError as ex:
                self.io.output(f"║ ValueError: {ex}!\n", 'error')
            else:
                success_connect = True
        return self.host, self.port

    def disconnect(self,):
        tuichat_utils.data_handler.Client.output(f'\nDisconnecting from {self.sock.getsockname()[0]} ...')
        try:
            self.freeze = True
            message = tuichat_utils.data_handler.Client.serialize_client_data('', self.uuid, 'disconnect')
            self.sock.sendall(bytes(message, encoding="utf-8"))
            self.sock.close()
        except Exception as ex:
            self.io.output(ex, 'error')
        else:
            self.io.output('Successfully disconnected from server! [OK]')
            answer = self.io.connect_input('disconnect')
            if answer:
                self.connect()
            else:
                exit()


if __name__ == '__main__':
    client = Client()
    client.main()
