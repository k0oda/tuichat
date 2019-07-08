class ConfigurationError(Exception):
    def __init__(self, text):
        self.output = f'ConfigurationError: {text}'
