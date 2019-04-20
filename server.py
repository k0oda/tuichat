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
        self.conn, self.addr = sock.accept()
        print(self.time(), "Подключен новый пользователь:", self.addr[0])

    def get_data(self, conn, addr,):
        while True:
            try:
                data = conn.recv(48634).decode('utf-8')
                if data:
                    print(self.time(), addr[0], "-", data)
                    conn.send(bytes("Server: Сообщение получено!", encoding="utf-8"))
            except ConnectionResetError:
                conn.close()
                print(self.time(), addr[0], "отключен!")
                break
            except ConnectionAbortedError:
                conn.close()
                print(self.time(), addr[0], "отключился!")
                break


server = Server()
while True:
    connection = Thread(target=server.accept())
    connection.start()
    user = Thread(target=server.get_data, args=(server.conn, server.addr,))
    user.start()
