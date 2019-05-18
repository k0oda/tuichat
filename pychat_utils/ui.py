class Server_infotable():
    def get_infotable(time, port, max_connections, external_ip, enable_log, enable_ui):
        infotable = f"""║ {time}
║ Server activated!
║ Port: {port}
║ Server limit of connections: {max_connections}
║ External IP address: {external_ip}
║ Logging: {enable_log}
║ UI symbols: {enable_ui}
"""
        return infotable

    def get_raw_infotable(time, port, max_connections, external_ip, enable_log, enable_ui):
        raw_infotable = f"""
{time}                                      
Server activated!                             
Port: {port}                                  
Server limit of connections: {max_connections}
External IP address: {external_ip}            
Logging: {enable_log}
UI symbols: {enable_ui}

"""
        return raw_infotable


class Logo():
    def get_logo(program_type):
        program_type = program_type.lower().replace(" ", "")
        if program_type == 'server':
            logo = """
 _____ __ __ _____ _       _   
|  _  |  |  |     | |_ ___| |_ 
|   __|_   _|   --|   | .'|  _|
|__|    |_| |_____|_|_|__,|_|                                                                                          
 ___ ___ ___ _ _ ___ ___       
|_ -| -_|  _| | | -_|  _|      
|___|___|_|  \_/|___|_|     
"""
        elif program_type == 'client':
            logo = """
 _____ __ __ _____ _       _   
|  _  |  |  |     | |_ ___| |_ 
|   __|_   _|   --|   | .'|  _|
|__|    |_| |_____|_|_|__,|_|                               
     _ _         _             
 ___| |_|___ ___| |_           
|  _| | | -_|   |  _|          
|___|_|_|___|_|_|_|                  
"""
        return logo

    def get_raw_logo(program_type):
        program_type = program_type.lower().replace(" ", "")
        if program_type == "server":
            logo = "PYChat.Server\n"
        elif program_type == "client":
            logo = "PYChat.Client\n"
        return logo


class License():
    def get_license():
        license = """
┌────────────────────────────────────────────────────────────────┐
│ PYChat  Copyright (C) 2019  Greenfield                         │
│ This program comes with ABSOLUTELY NO WARRANTY.                │
│ This is free software, and you are welcome to redistribute it  │
│ under certain conditions.                                      │
└────────────────────────────────────────────────────────────────┘
"""
        return license

    def get_raw_license():
        license = """
PYChat  Copyright (C) 2019  Greenfield
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
        return license


class Connection_info():
    def get_connection_info(host, port):
        connection_info = f"""║ Connection established!
║ Host: {host}
║ Port: {port}
"""
        return connection_info

    def get_raw_connection_info(host, port):
        raw_connection_info = f"""Connection established!
Host: {host}
Port: {port}
"""
        return raw_connection_info