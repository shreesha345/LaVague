class DriverException(Exception):
    pass


class CannotBackException(DriverException):
    def __init__(self, message="History root reached, cannot go back"):
        super().__init__(message)
