from app.shared.exception import AppException

class CustomerInvalidCredentialsERR(AppException):
    msg = "invalid credentials provided"
    code = 401


class CustomerInvalidEmailERR(AppException):
    msg = 'email must be at least 3 and no more than 50 characters long'
    code = 400


class CustomerInvalidNameERR(AppException):
    msg = 'username must be at least 3 and no more than 20 characters long'
    code = 400


class CustomerInvalidPasswordERR(AppException):
    msg = 'the password must be at least 8 and no more than 70 characters long. It must contain a capital letter, at least one number, and a special character (#?!@$%^&*-)'
    code = 400