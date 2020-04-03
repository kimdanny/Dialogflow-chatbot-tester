class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self):
        super().__init__()


class TestFailError(Error):
    """Raised when test is failed"""

    def __init__(self, msg):
        print(msg)


class StatusCodeError(Error):
    """Raised when HTTTP Status code is not 200"""

    def __init__(self, msg):
        print(msg)
