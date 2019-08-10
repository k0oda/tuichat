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
    def __init__(self,
                 mode='cli',
                 show_logo=True,
                 show_license=True,
                 show_connection_info=True,
                 msg_timeout=0.1,
                 server_host=None,
                 server_port=None
                 ):
        self.MODE = mode
        self.SHOW_LOGO = show_logo
        self.SHOW_LICENSE = show_license
        self.SHOW_CONNECTION_INFO = show_connection_info
        self.MSG_TIMEOUT = msg_timeout

        self.PUBKEY, self.PRIVKEY = rsa.newkeys(512)
        self.data_queue = []
        self.freeze = False                     # Variable for freezing io modules
        self.MSG_MAX_SYMBOLS = 300

        self.SERVER_CLOSED_EXCEPTIONS = (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)

        if self.MODE.lower() == 'gui':
            self.IO = tuichat_utils.io.Client.GUI
        else:
            self.IO = tuichat_utils.io.Client.CLI

        if self.SHOW_LOGO:
            logo_obj = tuichat_utils.ui.Logo('client')
            self.LOGO = logo_obj.logo

        if self.SHOW_LICENSE:
            license_obj = tuichat_utils.ui.License()
            self.COPYRIGHT = license_obj.license

        if server_host is not None and server_port is not None:
            self.connect(server_host, server_port)

    def main(self):
        if self.SHOW_LOGO:
            self.IO.output(self.LOGO)
        if self.SHOW_LICENSE:
            self.IO.output(self.COPYRIGHT)

        self.connect()
        self.start_client()

    def connect(self, host=None, port=None):
        if self.sock:
            self.sock.close()
            del self.sock
        self.sock = socket()

        success_connect = False
        while not success_connect:
            try:
                if self.MODE == 'cli' and host is None and port is None:
                    self.host = self.IO.connect_input('host')
                    self.port = self.IO.connect_input('port')
                elif host is not None and port is not None:
                    self.host = host
                    self.port = port
                else:
                    raise AttributeError('No host or port defined')
                self.sock.connect((self.host, self.port))
                self.setup_connection()
            except KeyboardInterrupt:
                exit()
            else:
                success_connect = True

        if self.MODE == 'cli':
            tuichat_utils.data_handler.clear_screen()
            if self.SHOW_LOGO:
                self.IO.output(self.LOGO)
            if self.SHOW_LICENSE:
                self.IO.output(self.COPYRIGHT)
            if self.SHOW_CONNECTION_INFO:
                connection_info_obj = tuichat_utils.ui.ConnectionInfo(self.host, self.port)
                connection_info = connection_info_obj.connection_info
                self.IO.output(connection_info)

        return self.host, self.port

    def setup_connection(self):
        self.sock.setblocking(False)
        self.sock.settimeout(5)                 # Getting handshake data timeout
        self.exchange_data()
        self.sock.settimeout(self.MSG_TIMEOUT)  # Main timeout

    def exchange_data(self):
        uuid_bytes = self.sock.recv(16)
        self.uuid = str(UUID(bytes=uuid_bytes))

        self.server_pub = self.sock.recv(172).decode('utf-8')

        self.sock.send(bytes(str(self.PUBKEY), encoding='utf-8'))

    def start_client(self):
        try:
            self.send_data()
        except Exception as ex:
            self.disconnect()
            if ex not in (KeyboardInterrupt, SystemExit):
                raise ex

    def send_data(self):
        while not self.freeze:
            try:
                self.receive_data()
                Timer(1.0, self.receive_data).start()

                message_input = self.init_prompt()

                if len(message_input) > self.MSG_MAX_SYMBOLS:
                    self.IO.output(f'║ The number of symbols of your message is more than {self.MSG_MAX_SYMBOLS}, '
                                   f'using first {self.MSG_MAX_SYMBOLS} symbols')
                    message_input = message_input[:self.MSG_MAX_SYMBOLS]

                if message_input == "/r":
                    self.print_data()
                else:
                    message = tuichat_utils.data_handler.Client.serialize_client_data(
                        message_input,
                        self.uuid,
                        'message'
                    )
                    self.sock.sendall(bytes(message, encoding="utf-8"))
            except self.SERVER_CLOSED_EXCEPTIONS:
                self.handle_server_closed()

    def init_prompt(self):
        if self.data_queue:
            prompt = f'You have [{len(self.data_queue)}] messages. Enter a message or enter "/r" to print new messages > '
        else:
            prompt = 'Enter a message > '
        return input(prompt)

    def receive_data(self):
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
                        self.data_queue.append(
                            f'{tuichat_utils.data_handler.get_time()} {data_dict["sender_address"]} - {data_dict["message"]}')
            except timeout:
                return
            except self.SERVER_CLOSED_EXCEPTIONS:
                self.handle_server_closed()

    def print_data(self):
        for data in self.data_queue:
            self.IO.output(data)
        self.data_queue.clear()

    def handle_server_closed(self):
        self.IO.output("\n║ Server closed!")
        self.freeze = True
        connect_again = self.IO.connect_input('reconnect')
        if connect_again:
            respond = self.reconnect()
            if respond is True:
                self.IO.output("║ Connection established!\n")
                self.freeze = False
                self.start_client()
            else:
                self.IO.output("\n║ Server did not respond!")
                self.IO.exit()
        else:
            exit()

    def reconnect(self):
        i = 0
        pbar = tqdm(total=5)
        while i <= 5:
            try:
                self.connect(self.host, self.port)
            except Exception as ex:
                self.IO.output(ex, 'error')
                sleep(1)
                i += 1
                pbar.update(1)
                continue
            else:
                pbar.close()
                return True
        else:
            pbar.close()
            return False

    def disconnect(self):
        self.IO.output(f'\nDisconnecting from {self.sock.getsockname()[0]} ...')
        try:
            self.freeze = True
            message = tuichat_utils.data_handler.Client.serialize_client_data('', self.uuid, 'disconnect')
            self.sock.sendall(bytes(message, encoding="utf-8"))
            self.sock.close()
        except Exception as ex:
            self.IO.output(ex, 'error')
        else:
            self.IO.output('Successfully disconnected from server! [OK]')
            answer = self.IO.connect_input('disconnect')
            if answer:
                self.connect()
            else:
                exit()


if __name__ == '__main__':
    client = Client()
    client.main()
