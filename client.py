from socket import socket
from threading import Thread

host = "localhost"
port = 3456
sock = socket()
sock.connect((host, port))
print(f"""
+=======================+
Connection established!
Host: {host}
Port: {port}
+=======================+
""")


class Client:
    def receive_data(self):
        data = sock.recv(48634).decode("utf-8")
        print(data)

    def send_data(self):
        message = input('Enter a message or enter "/r" to receive new messages > ')
        if message != "/r":
            sock.send(bytes(message, encoding="utf-8"))
        else:
            self.receive_data()


client = Client()
while True:
    sending = Thread(target=client.send_data())
    sending.start()
