from json import loads


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
{self.design_line} Press [CTRL + C] to stop server
'''
        self.raw_infotable = self.infotable.replace(self.design_line, '')


class Logo():
    def __init__(self, program_type):
        program_type = program_type.lower().replace(" ", "")
        if program_type == 'server':
            self.raw_logo = 'PYChat Server\n'
            self.logo = open('pychat_utils/tui_elements/server_logo.txt').read()
        elif program_type == 'client':
            self.raw_logo = 'PYChat Client\n'
            self.logo = open('pychat_utils/tui_elements/client_logo.txt').read()


class License():
    def __init__(self):
        self.raw_license = open('pychat_utils/tui_elements/copyright.txt').read()

        lines = self.raw_license.splitlines()
        max_lines = max(len(i) for i in lines)

        symbols_file = open('pychat_utils/tui_elements/block_symbols.json').read()
        symbols = loads(symbols_file)
        license_top = f'{symbols[0]}' + f'{symbols[1]}' * (max_lines) + f'{symbols[2]}'
        license_body = []
        for line in lines:
            line_separator = '' if line == lines[-1] else '\n'
            license_line = ''.join(symbols[4] + line.center(max_lines) + symbols[4] + line_separator)
            license_body.append(license_line)
        license_body = ''.join(license_body)
        license_bottom = f'{symbols[3]}' + f'{symbols[1]}' * (max_lines) + f'{symbols[5]}'

        self.license = f'{license_top}\n{license_body}\n{license_bottom}'


class ConnectionInfo():
    design_line = '║'
    def __init__(self, host, port):
        self.connection_info = f"""{self.design_line} Connection established!
{self.design_line} Host: {host}
{self.design_line} Port: {port}
"""
        self.raw_connection_info = self.connection_info.replace(self.design_line, '')
