import sqlite3
from argon2.exceptions import VerifyMismatchError
class TaskNotFound(Exception):
    pass
class TaskAlreadyExists(Exception):
    pass
class UserAlreadyExists(sqlite3.IntegrityError):
    pass
class InvalidEmail(Exception):
    pass
class InvalidPassword(Exception):
    pass
class UserNotFound(Exception):
    pass
class PasswordMismatchError(VerifyMismatchError):
    pass