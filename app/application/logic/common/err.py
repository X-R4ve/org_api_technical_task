

class BaseError(Exception):
    def __init__(self, code: int, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code
        self.message = message


class ApplicationError(BaseError):
    pass
