from socket import socket, timeout, gaierror
from threading import Thread
from os import system, name
import pychat_ui


class Client:
    def clear_screen(self):
        system("cls" if name == 'nt' else 'clear')

    def receive_data(self):
        while True:
            try:
                data = sock.recv(1024).decode("utf-8")
                print(data)
            except timeout:
                break

    def send_data(self):
        while True:
            try:
                message = input('Enter a message or enter "/r" to receive new messages > ')
                if message.replace(" ", "") != "/r":
                    sock.sendall(bytes(message, encoding="utf-8"))
                else:
                    self.receive_data()
            except ConnectionResetError:
                print("\n║ Server closed!")
                input("\n║ Press any key to exit...")
                exit()


client = Client()
if __name__ == '__main__':
    logo = pychat_ui.logo.get_logo('client')
    print(logo)

    license = pychat_ui.license.get_license()
    print(license)

    sock = socket()
    success_connect = False

    # Try to connect to server
    while not success_connect:
        try:
            host = input("║ Enter host: ").strip()
            port = int(input("║ Enter port: ").strip())
            msg_timeout = 1.0
            sock.connect((host, port))
            sock.settimeout(msg_timeout)
        except gaierror:
            print("║ Host not found!\n")
        except ConnectionRefusedError:
            print("║ Host rejected connection request!\n")
        else:
            success_connect = True
    client.clear_screen()

    print(logo)
    print(license)

    connection_info = pychat_ui.connection_info.get_connection_info(host, port)
    print(connection_info)

    sending = Thread(target=client.send_data())
    sending.start()

    receiving = Thread(target=client.receive_data())
    receiving.start()
