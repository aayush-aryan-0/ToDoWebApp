from sqlite3 import connect,Connection
import os
from errors import *
from task import Task
from datetime import datetime
from argon2 import PasswordHasher
from dateformate import isHtmlFormat,isSqliteFormat

class ToDoDB:
    
    @staticmethod
    def __connect()->Connection:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
       
        resources_dir = os.path.join(BASE_DIR, "resources")
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
            
        DB_PATH = os.path.join(resources_dir, "todo.db")
        
        conn = sqlite3.connect(DB_PATH)
      
        conn.row_factory = sqlite3.Row 
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_text TEXT,
                reminderDatetime TEXT DEFAULT (datetime('now', 'localtime')),
                done INTEGER NOT NULL DEFAULT 0,
                reminded INTEGER NOT NULL DEFAULT 0,
                username TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')
        return conn

    @staticmethod
    def addTask(task: Task)->None:
        if not isinstance(task, Task):
            raise TypeError("task must be an object of class Task")
        
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "INSERT INTO todo(task_text,username) VALUES(?,?)", 
                (task.text,task.username)
            )
           
            task.id = cursor.lastrowid

    @staticmethod
    def deleteTask(task: Task)->None:
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("DELETE FROM todo WHERE id = ?", (task.id,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.id} not found.")

    @staticmethod
    def toggleDone(task: Task)->None:
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("UPDATE todo SET done = 1 - done WHERE id = ?", (task.id,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task ID {task.id} not found.")

    @staticmethod
    def updateTask(task: Task)->None:
        with ToDoDB.__connect() as conn:
            if task.reminderDatetime:
                cursor = conn.execute(
                    "UPDATE todo SET task_text  = ?, reminderDatetime=? , done = ? WHERE id = ?",
                    (task.text,task.reminderDatetime, task.done, task.id)
                )
            else:
                cursor = conn.execute(
                    "UPDATE todo SET task_text  = ? , done = ? WHERE id = ?",
                    (task.text, task.done, task.id)
                )
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.text} not found.")

    @staticmethod
    def toggleReminded(task: Task)->None:
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "UPDATE todo SET reminded = 1-reminded WHERE id = ?",
                (task.id,)
            )
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.text} not found.")
    

    @staticmethod
    def readToDoDB(username:str)->list:
        tasks = []
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("SELECT * FROM todo where username =?",(username,))
            for row in cursor.fetchall():
                reminderDateTime=row['reminderDatetime']
                if not (isHtmlFormat(reminderDateTime)):
                    reminderDateTime=reminderDateTime.replace(" ","T")[:-3]
                tasks.append(Task(id=row['id'],text=row['task_text'], reminderDatetime=reminderDateTime,done=bool(row['done']),reminded=bool(row['reminded'])))
        return tasks
    @staticmethod
    def readAllToDoDB()->list:
        tasks = []
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("SELECT * FROM todo ")
            for row in cursor.fetchall():
                tasks.append(Task(id=row['id'],text=row['task_text'], reminderDatetime=row['reminderDatetime'],done=bool(row['done']),reminded=bool(row['reminded'])))
        return tasks
    

class Users:
     
    @staticmethod
    def __connect()->Connection:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
       
        resources_dir = os.path.join(BASE_DIR, "resources")
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
            
        DB_PATH = os.path.join(resources_dir, "todo.db")
        
        connect = sqlite3.connect(DB_PATH)
      
        connect.row_factory = sqlite3.Row 
        
        connect.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        return connect

    @staticmethod
    def addUser(username:str,password:str,email:str)->None:
        try:
            ph=PasswordHasher()
            password=ph.hash(password)
            with Users.__connect() as conn:
                cursor = conn.execute(
                    "INSERT INTO users(username, password,email) VALUES(?, ?,?)", 
                    (username,password,email)
                )
        except sqlite3.IntegrityError as e:
            raise UserAlreadyExists


    @staticmethod
    def deleteUser(username:str)->None:
        with Users.__connect() as conn:
            cursor = conn.execute("DELETE FROM users WHERE username = ?", (username,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {username} not found.")

    @staticmethod
    def changePassword(username:str,password:str)->None:
        ph=PasswordHasher()
        password=ph.hash(password)
        with Users.__connect() as conn:
            cursor = conn.execute("UPDATE users SET password = ? WHERE username = ?", (password,username))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task ID {username} not found.")

    @staticmethod
    def changeEmail(username:str,email:str)->None:
        with Users.__connect() as conn:
            cursor = conn.execute("UPDATE users SET email = ? WHERE username = ?", (email,username))
            if cursor.rowcount == 0:
                raise UserNotFound(f"{username} not found.")
    
    @staticmethod
    def account(username:str,password:str)->None:
        with Users.__connect() as conn:
            ph=PasswordHasher()
            cursor=conn.execute("SELECT password FROM users WHERE username=?",(username,)).fetchone()
            if not cursor:
                raise UserNotFound("User Not Found")
            ph.verify(cursor[0],password)
            #return cursor
        

            
      

    