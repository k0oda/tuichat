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
        data = sock.recv(48634).decode("utf-8")
        print(data)

    def send_data(self):
        message = input('Введите сообщение или введите "/r" чтобы получить новые сообщения > ')
        if message != "/r":
            sock.send(bytes(message, encoding="utf-8"))
        else:
            self.receive_data()


client = Client()
while True:
    sending = Thread(target=client.send_data())
    sending.start()
