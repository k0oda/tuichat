from datetime import datetime
from socket import socket
from threading import Thread
from urllib import request
from json import loads, JSONDecodeError
from os import system, name
import pychat_ui


class Server:
    users = []

    def clear_screen(self):
        system("cls" if name == 'nt' else 'clear')

    def get_time(self):
        current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S ')
        return current_time

    def save_log(self, data, open_type):
        log_file = open("log.txt", open_type)
        log_file.write(data)
        log_file.close()

    def accept_new_clients(self):
        self.connection, self.address = sock.accept()
        self.users.append(self.connection)
        time = self.get_time()
        new_user_msg = f"{time} New user connected: {self.address[0]}"
        print(new_user_msg)
        self.send_messages(new_user_msg + "\n")

    def configure(self):
        while True:
            print("Would you like to configure server now? [Y/n]")
            answer = input("> ").lower().strip()
            if answer == "y":
                try:
                    self.clear_screen()
                    max_connections_input = int(input("Enter value for limit of connections > ").strip())
                    port_input = int(input("Enter port > ").strip())
                    enable_log_input = input("Enable log? (Y/n) > ").lower().strip()
                    if enable_log_input == "y":
                        enable_log_input = True
                    elif enable_log_input == 'n':
                        enable_log_input = False
                    else:
                        raise ValueError
                    enable_ui_input = input("Enable UI symbols? (Y/n) > ").lower().strip()
                    if enable_ui_input == "y":
                        enable_ui_input = True
                    elif enable_ui_input == 'n':
                        enable_ui_input = False
                    else:
                        raise ValueError
                    self.clear_screen()
                except ValueError:
                    self.clear_screen()
                    print("[ERROR] Error in data entry!")
                else:
                    return max_connections_input, port_input, enable_log_input, enable_ui_input
            elif answer == "n":
                self.clear_screen()
                print("Using standart variables...")
                return 5, 8000, False, False
            else:
                self.clear_screen()
                print("[ERROR] Unknown command!")

    def get_data(self, conn, address,):
        while True:
            try:
                self.data = conn.recv(1024).decode('utf-8')
                if self.data:
                    self.data = f"{self.get_time()} {address[0]} - {self.data}"
                    print(self.data)
                    self.send_messages(self.data + "\n")
            except ConnectionResetError:
                conn.close()
                self.users.remove(conn)
                connection_reset_msg = f"{self.get_time()} {address[0]} disconnected!"
                print(connection_reset_msg)
                self.send_messages(connection_reset_msg + "\n")
                break
            except ConnectionAbortedError:
                conn.close()
                self.users.remove(conn)
                connection_aborted_msg = f"{self.get_time()} {address[0]} disconnected!"
                print(connection_aborted_msg)
                self.send_messages(connection_aborted_msg + "\n")
                break

    def send_messages(self, message,):
        if enable_log:
            self.save_log(message, 'a')
        for user in self.users:
            user.sendall(bytes(message, encoding="utf-8"))


if __name__ == '__main__':
    server = Server()

    try:
        config = open('config.json').read()
        config = loads(config)
    except FileNotFoundError:
        print("[ERROR] Configuration file not found!")
        max_connections, port, enable_log, enable_ui = server.configure()
    except JSONDecodeError:
        print("[ERROR] JSON decoding error!")
        max_connections, port, enable_log, enable_ui = server.configure()
    else:
        try:
            max_connections = config[0]['max_connections']
            port = config[1]['port']
            enable_log = config[2]['enable_log']
            enable_log = bool(enable_log)
            enable_ui = config[3]['enable_ui']
            enable_ui = bool(enable_ui)
        except ValueError:
            print("[ERROR] Error in config file!")
            max_connections, port, enable_log, enable_ui = server.configure()

    sock = socket()
    sock.bind(("0.0.0.0", port))
    sock.listen(max_connections)
    external_ip = request.urlopen('http://ident.me').read().decode("utf-8")
    start_time = server.get_time()

    logo = pychat_ui.logo.get_logo('server') if enable_ui else pychat_ui.logo.get_raw_logo('server')
    print(logo)

    license = pychat_ui.license.get_license() if enable_ui else pychat_ui.license.get_raw_license()
    print(license)

    if enable_ui:
        info_table = pychat_ui.server_infotable.get_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        raw_info_table = pychat_ui.server_infotable.get_raw_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        if enable_log:
            server.save_log(raw_info_table, 'w')
    else:
        info_table = pychat_ui.server_infotable.get_raw_infotable(start_time, port, max_connections, external_ip, enable_log, enable_ui)
        if enable_log:
            server.save_log(info_table, 'w')
    print(info_table)
    while True:  # Infinity accepting new connections and receiving data
        connection = Thread(target=server.accept_new_clients())
        connection.start()
        get_msg = Thread(target=server.get_data, args=(server.connection, server.address,))
        get_msg.start()
