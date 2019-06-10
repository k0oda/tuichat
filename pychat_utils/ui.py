class ServerInfotable():
    design_line = '║'
    def __init__(self, time, port, max_connections, external_ip, enable_log, enable_ui):
        self.infotable = f'''
{self.design_line} {time}
{self.design_line} Server activated!
{self.design_line} Port: {port}
{self.design_line} Limit of connections: {max_connections}
{self.design_line} External IP address: {external_ip}
{self.design_line} Logging: {enable_log}
{self.design_line} UI symbols: {enable_ui}
'''
        self.raw_infotable = self.infotable.replace(self.design_line, '')


class Logo():
    def __init__(self, program_type):
        program_type = program_type.lower().replace(" ", "")
        if program_type == 'server':
            self.raw_logo = 'PYChat Server\n'
            self.logo = '''
 _____ __ __ _____ _       _   
|  _  |  |  |     | |_ ___| |_ 
|   __|_   _|   --|   | .'|  _|
|__|    |_| |_____|_|_|__,|_|                                                                                          
 ___ ___ ___ _ _ ___ ___       
|_ -| -_|  _| | | -_|  _|      
|___|___|_|  \_/|___|_|     
'''
        elif program_type == 'client':
            self.raw_logo = 'PYChat Client\n'
            self.logo = '''
 _____ __ __ _____ _       _   
|  _  |  |  |     | |_ ___| |_ 
|   __|_   _|   --|   | .'|  _|
|__|    |_| |_____|_|_|__,|_|                               
     _ _         _             
 ___| |_|___ ___| |_           
|  _| | | -_|   |  _|          
|___|_|_|___|_|_|_|                  
'''


class License():
    def __init__(self):
        self.license = """
┌────────────────────────────────────────────────────────────────┐
│ PYChat  Copyright (C) 2019  Greenfield                         │
│ This program comes with ABSOLUTELY NO WARRANTY.                │
│ This is free software, and you are welcome to redistribute it  │
│ under certain conditions.                                      │
└────────────────────────────────────────────────────────────────┘
"""
        self.raw_license = """
PYChat  Copyright (C) 2019  Greenfield
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""


class ConnectionInfo():
    design_line = '║'
    def __init__(self, host, port):
        self.connection_info = f"""║ Connection established!
║ Host: {host}
║ Port: {port}
"""
        self.raw_connection_info = self.connection_info.replace(design_line, '')
