from app.shared.exception import AppException

class CustomerAlreadyAuthorizedERR(AppException):
    msg = "you are already logged in"
    code = 409