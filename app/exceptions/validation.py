

class ValidationErrorException(Exception):
    def __init__(self, errors: list):
        details = []
        self.details = [
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
            for error in errors
        ]

        super().__init__("Request validation failed")
