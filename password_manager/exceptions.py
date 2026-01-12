# COMMON
class InvalidArgumentException(Exception):
    pass
class GracefulShutdownException(Exception):
    pass
class UserLogoutException(Exception):
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