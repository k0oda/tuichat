from socket import socket, timeout
from threading import Thread
from os import system, name


def clear():
    system("cls" if name == 'nt' else 'clear')


logo = """
 ______   __  __     ______     __  __     ______     ______  
/\  == \ /\ \_\ \   /\  ___\   /\ \_\ \   /\  __ \   /\__  _\ 
\ \  _-/ \ \____ \  \ \ \____  \ \  __ \  \ \  __ \  \/_/\ \/ 
 \ \_\    \/\_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\    \ \_\ 
  \/_/     \/_____/   \/_____/   \/_/\/_/   \/_/\/_/     \/_/ 

"""

# License
license = """
┌────────────────────────────────────────────────────────────────┐
│ PYChat  Copyright (C) 2019  Greenfield                         │
│ This program comes with ABSOLUTELY NO WARRANTY.                │
│ This is free software, and you are welcome to redistribute it  │
│ under certain conditions.                                      │
└────────────────────────────────────────────────────────────────┘
"""

print(logo)
print(license)

host = input("Enter host: ").strip()
port = int(input("Enter port: ").strip())
msg_timeout = 1.0
sock = socket()
sock.connect((host, port))
sock.settimeout(msg_timeout)
clear()
print(logo)
print(license)
print(f"""
║ Connection established!
║ Host: {host}
║ Port: {port}
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
