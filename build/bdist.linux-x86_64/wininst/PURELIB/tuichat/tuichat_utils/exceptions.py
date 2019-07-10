class ConfigurationError(Exception):
    def __init__(self, text):
        self.output = f'ConfigurationError: {text}'


class InputTypeError(Exception):
    def __init__(self, text):
        self.output = f'InputTypeError: {text}'
