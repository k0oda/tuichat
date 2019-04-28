from datetime import datetime
from socket import socket
from threading import Thread
from urllib import request
from json import loads, JSONDecodeError
from os import system, name

def clear():
    system("cls" if name == 'nt' else 'clear')

def configure(configure):
    while configure == True:
        print("Would you like to configure server now? [Y/n]")
        answer = input("> ").lower().replace(" ", "")
        if answer == "y":
            try:
                clear()
                max_connections = int(input("Enter value limit of connections > ").replace(" ", ""))
                port = int(input("Enter port > ").replace(" ", ""))
                clear()
            except TypeError:
                print("[ERROR] Answer must be only a number!")
            finally:
                return max_connections, port
                configure = False
        elif answer == "n":
            configure = False
            clear()
            print("Using standart variables...")
            return 5, 8000
        else:
            clear()
            print("[ERROR] Unknown command!")

try:
    config = open('config.json').read()
    config = loads(config)
except FileNotFoundError:
    print("[ERROR] Configuration file not found!")
    max_connections, port = configure(True)
except JSONDecodeError:
    print("[ERROR] JSON deserialization error!")
    max_connections, port = configre(True)
else:
    max_connections = config[0]['max_connections']
    port = config[1]['port']

sock = socket()
sock.bind(("", port))
sock.listen(max_connections)
external_ip = request.urlopen('http://ident.me').read().decode("utf-8")

# License
print("""
PYChat  Copyright (C) 2019  Greenfield
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
""")

print(f"""
+======================================================+
Server activated!
Port: {port}
Server limit of connections: {max_connections}
External IP address: {external_ip}
+======================================================+
""")


class Server:
    users = []

    def time(self):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S |')
        return current_time

    def accept(self):
        self.connection, self.address = sock.accept()
        self.users.append(self.connection)
        new_user_msg = f"{self.time()} New user connected: {self.address[0]}"
        print(new_user_msg)
        self.send_messages(new_user_msg + "\n")

    def get_data(self, connection, address,):
        while True:
            try:
                self.data = connection.recv(48634).decode('utf-8')
                if self.data:
                    self.data = f"{self.time()} {address[0]} - {self.data}"
                    print(self.data)
                    self.send_messages(self.data + "\n")
            except ConnectionResetError:
                connection.close()
                connection_reset_msg = f"{self.time()} {address[0]} disconnected!"
                print(connection_reset_msg)
                self.send_messages(connection_reset_msg + "\n")
                break
            except ConnectionAbortedError:
                connection.close()
                connection_aborted_msg = f"{self.time()} {address[0]} disconnected!"
                print(connection_aborted_msg)
                self.send_messages(connection_aborted_msg + "\n")
                break

    def send_messages(self, message,):
        for user in self.users:
            try:
                user.send(bytes(message, encoding="utf-8"))
            except OSError:
                user.close()


server = Server()
while True:  # Infinity accepting new connections and receiving data
    connection = Thread(target=server.accept())
    connection.start()
    get_msg = Thread(target=server.get_data, args=(server.connection, server.address,))
    get_msg.start()
