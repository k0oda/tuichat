#!/usr/bin/env python3

from tuichat_utils import ui, data_handler
from socket import socket, timeout, gaierror
from threading import Timer
from json import loads
from tqdm import tqdm
from time import sleep


class Client:
    data_queue = []
    freeze = False

    def main(self,):
        self.msg_max_symbols = 300

        logo_obj = ui.Logo('client')
        logo = logo_obj.logo
        print(logo)

        license_obj = ui.License()
        copyright = license_obj.license
        print(copyright)

        host, port = self.connect()
        data_handler.clear_screen()
        print(logo)
        print(copyright)

        connection_info_obj = ui.ConnectionInfo(host, port)
        connection_info = connection_info_obj.connection_info
        print(connection_info)

        try:
            self.send_data()
        except (KeyboardInterrupt, SystemExit):
            self.disconnect()
        except Exception as ex:
            print(ex)
            self.disconnect()

    def receive_data(self,):
        if not self.freeze:
            try:
                data = self.sock.recv(1128).decode('utf-8')
                data = data.split(self.uuid)
                data = data[:-1]
                for element in data:
                    data_dict = loads(element)
                    self.data_queue.append(f'{data_handler.get_time()} {data_dict["sender_address"]} - {data_dict["message"]}')
            except timeout:
                return

    def print_data(self,):
        for data in self.data_queue:
            print(data)
        self.data_queue.clear()

    def send_data(self,):
        while True:
            try:
                message_input = input('Enter a message or enter "/r" to receive new messages > ')
                Timer(1.0, self.receive_data).start()
                if len(message_input) > self.msg_max_symbols:
                    print(f'║ The number of symbols of your message is more than {self.msg_max_symbols}, using first {self.msg_max_symbols} symbols')
                    message_input = message_input[:self.msg_max_symbols]

                if message_input != "/r":
                    message = data_handler.Client.serialize_client_data(message_input, self.uuid)
                    self.sock.sendall(bytes(message, encoding="utf-8"))
                else:
                    self.print_data()
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                print("\n║ Server closed!")
                self.freeze = True
                connect_again = input("Try to connect again? (Y/n) > ").lower().strip()
                if connect_again == "y":
                    respond = self.reconnect()
                    if respond is True:
                        print("║ Connection established!\n")
                        self.freeze = False
                        continue
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
                pbar.close()
                return True
        else:
            pbar.close()
            return False

    def connect(self, success_connect=False,):
        self.sock = socket()

        while not success_connect:
            try:
                self.host = input("║ Enter host: ").strip()
                self.port = int(input("║ Enter port: ").strip())
                msg_timeout = 0.1
                self.sock.connect((self.host, self.port))
                self.sock.setblocking(0)
                self.sock.settimeout(5)
                uuid = self.sock.recv(256).decode('utf-8')
                self.sock.settimeout(msg_timeout)
            except gaierror:
                print("║ Host not found!\n")
            except (ConnectionRefusedError, timeout, TimeoutError):
                print("║ Host rejected connection request!\n")
            except ValueError:
                print("║ Incorrect value!\n")
            else:
                uuid = loads(uuid)
                self.uuid = uuid['uuid']
                success_connect = True
        return self.host, self.port

    def disconnect(self,):
        print(f'\nDisconnecting from {self.sock.getsockname()[0]} ...')
        try:
            self.sock.close()
        except Exception as ex:
            print(ex)
        else:
            print('Successfully disconnected from server! [OK]')
            input('Press any key to exit ...')
            exit()


if __name__ == '__main__':
    client = Client()
    client.main()
