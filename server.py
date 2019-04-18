import socket

max_connections = 5
port = 3456
sock = socket.socket()
sock.bind(("", port))
sock.listen(max_connections)
sock.setblocking(0)

print(f"""
+======================================================+
Server activated!
Port: {port}
Server limit of connections: {max_connections}
+======================================================+
""")


def accept():
    conn, addr = sock.accept()
    print("Подключен новый пользователь:", addr[0])
    return conn, addr


while True:
    try:
        conn, addr = accept()
        data = conn.recv(48634).decode('utf-8')
        print(addr[0], "-", data)
        # conn.send(bytes("Server: Сообщение получено!", encoding="utf-8"))
    except ConnectionResetError:
        print(addr[0], "отключился!")
        conn, addr = accept()
    except socket.error:
        pass
