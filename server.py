from datetime import datetime
from socket import socket
from threading import Thread
from urllib import request
from json import loads, JSONDecodeError
from os import system, name


def time():
    current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S |')
    return current_time


def clear():
    system("cls" if name == 'nt' else 'clear')


def save_log(data, open_type):
    log_file = open("log.txt", open_type)
    log_file.write(data)
    log_file.close()


def configure():
    while True:
        print("Would you like to configure server now? [Y/n]")
        answer = input("> ").lower().strip()
        if answer == "y":
            try:
                clear()
                max_connections_input = int(input("Enter value for limit of connections > ").strip())
                port_input = int(input("Enter port > ").strip())
                enable_log_input = input("Enable log? (Y/n) > ").lower().strip()
                if enable_log_input == "y":
                    enable_log_input = True
                elif enable_log_input == 'n':
                    enable_log_input = False
                else:
                    raise ValueError
                clear()
            except ValueError:
                clear()
                print("[ERROR] Error in data entry!")
            else:
                return max_connections_input, port_input, enable_log_input
        elif answer == "n":
            clear()
            print("Using standart variables...")
            return 5, 8000, False
        else:
            clear()
            print("[ERROR] Unknown command!")


try:
    config = open('config.json').read()
    config = loads(config)
except FileNotFoundError:
    print("[ERROR] Configuration file not found!")
    max_connections, port, enable_log = configure()
except JSONDecodeError:
    print("[ERROR] JSON deserialization error!")
    max_connections, port, enable_log = configure()
else:
    max_connections = config[0]['max_connections']
    port = config[1]['port']
    enable_log = config[2]['enable_log']
    enable_log = bool(enable_log)

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

info_table = f"""+======================================================+
{time()}
Server activated!
Port: {port}
Server limit of connections: {max_connections}
External IP address: {external_ip}
Logging: {enable_log}
+======================================================+
"""
print(info_table)
if enable_log:
    save_log(info_table, 'w')


class Server:
    users = []

    def accept(self):
        self.connection, self.address = sock.accept()
        self.users.append(self.connection)
        new_user_msg = f"{time()} New user connected: {self.address[0]}"
        print(new_user_msg)
        self.send_messages(new_user_msg + "\n")

    def get_data(self, conn, address,):
        while True:
            try:
                self.data = conn.recv(48634).decode('utf-8')
                if self.data:
                    self.data = f"{time()} {address[0]} - {self.data}"
                    print(self.data)
                    self.send_messages(self.data + "\n")
            except ConnectionResetError:
                conn.close()
                self.users.remove(conn)
                connection_reset_msg = f"{time()} {address[0]} disconnected!"
                print(connection_reset_msg)
                self.send_messages(connection_reset_msg + "\n")
                break
            except ConnectionAbortedError:
                conn.close()
                self.users.remove(conn)
                connection_aborted_msg = f"{time()} {address[0]} disconnected!"
                print(connection_aborted_msg)
                self.send_messages(connection_aborted_msg + "\n")
                break

    def send_messages(self, message,):
        if enable_log:
            save_log(message, 'a')
        for user in self.users:
            user.send(bytes(message, encoding="utf-8"))


server = Server()
while True:  # Infinity accepting new connections and receiving data
    connection = Thread(target=server.accept())
    connection.start()
    get_msg = Thread(target=server.get_data, args=(server.connection, server.address,))
    get_msg.start()
