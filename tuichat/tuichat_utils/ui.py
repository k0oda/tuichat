import importlib.resources as pkg_resources
from json import loads
from string import Template
from . import tui_elements


class ServerInfotable:
    design_line = '║'

    def __init__(self, time, port, max_connections, external_ip, enable_log, enable_ui, version):
        self.raw_infotable = pkg_resources.read_text(tui_elements, 'server_infotable_message.txt')
        lines = self.raw_infotable.splitlines()

        complete_lines = []
        for line in lines:
            line = f'{self.design_line} {line}\n'
            complete_lines.append(line)

        t = Template(''.join(complete_lines))
        self.infotable = t.substitute(
            time=time, port=port, max_connections=max_connections,
            external_ip=external_ip, enable_log=enable_log, enable_ui=enable_ui,
            version=version
        )


class Logo:
    def __init__(self, program_type):
        program_type = program_type.lower().replace(" ", "")
        if program_type == 'server':
            self.raw_logo = 'TuiChat Server\n'
            self.logo = pkg_resources.read_text(tui_elements, 'server_logo.txt')
        elif program_type == 'client':
            self.raw_logo = 'TuiChat Client\n'
            self.logo = pkg_resources.read_text(tui_elements, 'client_logo.txt')


class License:
    def __init__(self):
        self.raw_license = pkg_resources.read_text(tui_elements, 'copyright.txt')

        lines = self.raw_license.splitlines()
        max_lines = max(len(i) for i in lines)

        symbols_file = pkg_resources.read_text(tui_elements, 'block_symbols.json')
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


class ConnectionInfo:
    design_line = '║'

    def __init__(self, host, port):
        self.connection_info = f"""{self.design_line} Connection established!
{self.design_line} Host: {host}
{self.design_line} Port: {port}
"""
        self.raw_connection_info = self.connection_info.replace(self.design_line, '')
