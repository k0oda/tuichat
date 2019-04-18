import socket
from threading import Thread

max_connections = 5
port = 3456
sock = socket.socket()
sock.bind(("", port))
sock.listen(max_connections)

print(f"""
+======================================================+
Server activated!
Port: {port}
Server limit of connections: {max_connections}
+======================================================+
""")


class Server:
    def accept(self):
        self.conn, self.addr = sock.accept()
        print("Подключен новый пользователь:", self.addr[0])

    def get_data(self, conn, addr,):
        while True:
            try:
                data = conn.recv(48634).decode('utf-8')
                print(addr[0], "-", data)
                conn.send(bytes("Server: Сообщение получено!", encoding="utf-8"))
            except ConnectionResetError:
                print(addr[0], "отключен!")
                break
            except ConnectionAbortedError:
                print(addr[0], "отключился!")
                break


while True:
    connection = Thread(target=Server.accept(Server))
    connection.start()
    user = Thread(target=Server.get_data, args=(Server, Server.conn, Server.addr,))
    user.start()
