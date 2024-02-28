class BaseEsiException(Exception):
    def __init__(self, err_msg: str | None = None):
        self.err_msg = err_msg
        super().__init__(err_msg)


class AuthException(BaseEsiException):
    pass

class EsiException(BaseEsiException):
    pass