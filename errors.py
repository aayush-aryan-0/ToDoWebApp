import sqlite3
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