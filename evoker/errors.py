from sanic.exceptions import SanicException

class InvalidRequst(SanicException):
    status_code = 400

    @property
    def message(self):
        return "Invalid request: missing field '{}'".format(self.extra["missing"])

class InvalidAmountError(SanicException):
    status_code = 400

    @property
    def message(self):
        return "Invalid amount: must be between 1 and 10"