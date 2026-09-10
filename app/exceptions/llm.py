class LlmUnavailableException(Exception):
    def __init__(self):
        super().__init__("Language model is unavailable")