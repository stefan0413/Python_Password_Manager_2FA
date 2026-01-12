# COMMON
class InvalidArgumentException(Exception):
    pass

# REGISTRATION
class RegistrationException(Exception):
   pass

class UserAlreadyExistsException(RegistrationException):
    pass

class PasswordsDoNotMatch(RegistrationException):
    pass

# LOGIN
class LoginException(Exception):
    pass

class UserDoesNotExistException(LoginException):
    pass