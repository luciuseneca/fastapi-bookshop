from app.shared.exception import AppException

class CustomerNotActiveERR(AppException):
    msg = "user unavailable"
    code = 400