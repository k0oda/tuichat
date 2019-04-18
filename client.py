import socket

sock = socket.socket()
sock.connect(("localhost", 3456))
input("Подключено! Нажмите для отправки")
while True:
    your_data = input("Введите сообщение для отправки на сервер: ")
    bin_data = bytes(your_data, encoding="utf-8")
    sock.send(bin_data)
    data = sock.recv(16384)
    print("Сообщение от сервера:", data.decode("utf-8"))
