from socket import socket, timeout
from threading import Thread

host = "localhost"
port = 3456
msg_timeout = 1.0
sock = socket()
sock.connect((host, port))
sock.settimeout(msg_timeout)
print(f"""
+=======================+
Connection established!
Host: {host}
Port: {port}
+=======================+
""")


class Client:
    def receive_data(self):
        try:
            data = sock.recv(48634).decode("utf-8")
            print(data)
        except timeout:
            print("No new messages! \n")


    def send_data(self):
        message = input('Enter a message or enter "/r" to receive new messages > ')
        if message.replace(" ", "") != "/r":
            sock.send(bytes(message, encoding="utf-8"))
        else:
            self.receive_data()


client = Client()
while True:
    sending = Thread(target=client.send_data())
    sending.start()
