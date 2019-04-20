from datetime import datetime
from socket import socket
from threading import Thread
from urllib import request

max_connections = 5
port = 3456
sock = socket()
sock.bind(("", port))
sock.listen(max_connections)
ip = request.urlopen('http://ident.me').read().decode("utf-8")

print(f"""
+======================================================+
Server activated!
Port: {port}
Server limit of connections: {max_connections}
External IP address: {ip}
+======================================================+
""")


class Server:
    def __init__(self):
        self.users = []

    def time(self):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S |')
        return current_time

    def accept(self):
        self.connection, self.address = sock.accept()
        self.users.append(self.connection)
        new_user_msg = f"{self.time()} Подключен новый пользователь: {self.address[0]}"
        print(new_user_msg)
        self.send_messages(new_user_msg)

    def get_data(self, connection, address,):
        while True:
            try:
                self.data = connection.recv(48634).decode('utf-8')
                if self.data:
                    self.data = f"{self.time()} {address[0]} - {self.data}"
                    print(self.data)
                    self.send_messages(self.data)
            except ConnectionResetError:
                connection.close()
                connection_reset_msg = f"{self.time()} {address[0]} отключен!"
                print(connection_reset_msg)
                self.send_messages(connection_reset_msg)
                break
            except ConnectionAbortedError:
                connection.close()
                connection_aborted_msg = f"{self.time()} {address[0]} отключился!"
                print(connection_aborted_msg)
                self.send_messages(connection_aborted_msg)
                break

    def send_messages(self, message,):
        for user in self.users:
            user.send(bytes(message, encoding="utf-8"))


server = Server()
while True:
    connection = Thread(target=server.accept())
    connection.start()
    user = Thread(target=server.get_data, args=(server.connection, server.address,))
    user.start()
