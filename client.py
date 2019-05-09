from socket import socket, timeout, gaierror
from threading import Thread
from os import system, name
from datetime import datetime
from json import dumps
import emoji
from tqdm import tqdm
import time
import sys
import pychat_ui


class Client:
    def get_time(self,):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S ')
        return current_time

    def clear_screen(self):
        system("cls" if name == 'nt' else 'clear')

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024).decode("utf-8")
                print(data)
            except timeout:
                break

    def send_data(self):
        while True:
            try:
                message_input = emoji.emojize(input('Enter a message or enter "/r" to receive new messages > '))
                if message_input.replace(" ", "") != "/r":
                    message = dumps({
                    "sending_time": self.get_time(),
                    "message": message_input})
                    self.sock.sendall(bytes(message, encoding="utf-8"))
                    respond = self.sock.recv(1).decode('utf-8')
                    if not respond:
                        raise ConnectionResetError
                else:
                    self.receive_data()
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                print("\n║ Server closed!")
                connect_again = input("Try to connect again? (Y/n) > ").lower().strip()
                if connect_again == "y":
                    respond = self.reconnect()
                    if respond == True:
                        print("\n║ Connection established!\n")
                        continue
                    else:
                        print("\n║ Server didn't respond!")
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

    def connect(self, success_connect = False):
        self.sock = socket()

        while not success_connect:
            try:
                self.host = input("║ Enter host: ").strip()
                self.port = int(input("║ Enter port: ").strip())
                msg_timeout = 1.0
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

    receiving = Thread(target=client.receive_data())
    receiving.start()
