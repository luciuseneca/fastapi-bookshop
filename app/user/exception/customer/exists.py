from app.shared.exception import AppException

class CustomerNotFoundERR(AppException):
    msg = "user not found"
    code = 404


class CustomerAlreadyExistsERR(AppException):
    msg = 'user with this email already exists'
    code = 409