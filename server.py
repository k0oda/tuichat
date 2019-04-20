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
    def time(self):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S |')
        return current_time

    def accept(self):
        self.connection, self.address = sock.accept()
        print(self.time(), "Подключен новый пользователь:", self.address[0])

    def get_data(self, connection, address,):
        while True:
            try:
                data = connection.recv(48634).decode('utf-8')
                if data:
                    print(self.time(), address[0], "-", data)
                    connection.send(bytes("Server: Сообщение получено!", encoding="utf-8"))
            except ConnectionResetError:
                connection.close()
                print(self.time(), address[0], "отключен!")
                break
            except ConnectionAbortedError:
                connection.close()
                print(self.time(), address[0], "отключился!")
                break


server = Server()
while True:
    connection = Thread(target=server.accept())
    connection.start()
    user = Thread(target=server.get_data, args=(server.connection, server.address,))
    user.start()
