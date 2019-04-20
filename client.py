from socket import socket
from threading import Thread

server_ip = "localhost"
port = 3456
sock = socket()
sock.connect((server_ip, port))
print(f"""
+=======================+
Соединение установлено!
Сервер: {server_ip}
Порт: {port}
+=======================+
""")


class Client:
    def receive_data(self):
        try:
            data = sock.recv(48634).decode("utf-8")
            print(data)
        except:
            pass

    def send_data(self):
        message = input("Ввод > ")
        sock.send(bytes(message, encoding="utf-8"))


client = Client()
while True:
    data = Thread(target=client.receive_data())
    data.start()
    sending = Thread(target=client.send_data())
    sending.start()
