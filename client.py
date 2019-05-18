from socket import socket, timeout, gaierror
from threading import Thread, Timer
from os import system, name
from datetime import datetime
from json import dumps, loads
from tqdm import tqdm
from time import sleep
import sys
import pychat_ui


class Client:
    data_list = []

    def clear_screen(self,):
        system("cls" if name == 'nt' else 'clear')

    def get_time(self,):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S ')
        return current_time

    def receive_data(self,):
        while True:
            try:
                data = self.sock.recv(65536).decode('utf-8')
                data = data.split('a3fd558d-9921-4176-8e9d-c0028642c549')
                data = data[:-1]
                for element in data:
                    data_dict = loads(element)
                    self.data_list.append(f'{self.get_time()} {data_dict["sender_address"]} - {data_dict["message"]}')
            except timeout:
                break

    def print_data(self,):
        for data in self.data_list:
            print(data)
        self.data_list.clear()

    def send_data(self,):
        while True:
            try:
                message_input = input('Enter a message or enter "/r" to receive new messages > ')
                Timer(1.0, self.receive_data).start()
                if message_input != "/r":
                    message = self.serialize_data(message_input)
                    self.sock.sendall(bytes(message, encoding="utf-8"))
                else:
                    self.print_data()
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                print("\n║ Server closed!")
                connect_again = input("Try to connect again? (Y/n) > ").lower().strip()
                if connect_again == "y":
                    respond = self.reconnect()
                    if respond == True:
                        print("║ Connection established!\n")
                        continue
                    else:
                        print("\n║ Server did not respond!")
                        input("Press any key to exit...")
                        exit()
                else:
                    exit()

    def serialize_data(self, message,):
        message_dict = {
            "message": message
            }
        serialized_dict = dumps(message_dict) + 'a3fd558d-9921-4176-8e9d-c0028642c549'
        return serialized_dict

    def reconnect(self,):
        i = 0
        pbar = tqdm(total=5)
        while i <= 5:
            try:
                self.sock.close()
                self.sock = socket()
                self.sock.connect((self.host, self.port))
            except:
                time.sleep(1)
                i += 1
                pbar.update(1)
                continue
            else:
                pbar.close()
                return True
        else:
            pbar.close()
            return False

    def connect(self, success_connect = False,):
        self.sock = socket()

        while not success_connect:
            try:
                self.host = input("║ Enter host: ").strip()
                self.port = int(input("║ Enter port: ").strip())
                msg_timeout = 0.1
                self.sock.connect((self.host, self.port))
                self.sock.settimeout(msg_timeout)
            except gaierror:
                print("║ Host not found!\n")
            except ConnectionRefusedError:
                print("║ Host rejected connection request!\n")
            except ValueError:
                print("║ Incorrect value!\n")
            else:
                success_connect = True
        return self.host, self.port


client = Client()
if __name__ == '__main__':
    logo = pychat_ui.logo.get_logo('client')
    print(logo)

    license = pychat_ui.license.get_license()
    print(license)

    host, port = client.connect()
    client.clear_screen()

    print(logo)
    print(license)

    connection_info = pychat_ui.connection_info.get_connection_info(host, port)
    print(connection_info)

    sending = Thread(target=client.send_data())
    sending.start()
