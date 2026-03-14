import sqlite3
import os
from errors import *
from task import Task
from datetime import datetime
from argon2 import PasswordHasher
class ToDoDB:
    
    @staticmethod
    def __connect():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
       
        resources_dir = os.path.join(BASE_DIR, "resources")
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
            
        DB_PATH = os.path.join(resources_dir, "todo.db")
        
        connect = sqlite3.connect(DB_PATH)
      
        connect.row_factory = sqlite3.Row 
        
        connect.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                reminderDatetime TEXT DEFAULT (datetime('now', 'localtime')),
                done INTEGER NOT NULL DEFAULT 0,
                reminded INTEGER NOT NULL DEFAULT 0
            )
        ''')
        return connect

    @staticmethod
    def addTask(task: Task):
        if not isinstance(task, Task):
            raise TypeError("task must be an object of class Task")
        
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "INSERT INTO todo(task,reminderDatetime,done,reminded) VALUES(?, ?,?,?)", 
                (task.text,task.reminderDatetime,task.done,task.reminded)
            )
           
            task.id = cursor.lastrowid

    @staticmethod
    def deleteTask(task: Task):
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("DELETE FROM todo WHERE id = ?", (task.id,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.id} not found.")

    @staticmethod
    def toggleDone(task: Task):
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("UPDATE todo SET done = 1 - done WHERE id = ?", (task.id,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task ID {task.id} not found.")

    @staticmethod
    def updateTask(task: Task):
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "UPDATE todo SET task = ?, datetime=? , done = ? WHERE id = ?",
                (task.text,task.reminderDatetime, task.done, task.id)
            )
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.text} not found.")

    @staticmethod
    def toggleReminded(task: Task):
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "UPDATE todo SET reminded = 1-reminded WHERE id = ?",
                (task.id,)
            )
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.text} not found.")
    

    @staticmethod
    def readToDoDB():
        tasks = []
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("SELECT * FROM todo")
            for row in cursor.fetchall():
                tasks.append(Task(id=row['id'],text=row['task'], reminderDatetime=datetime.fromisoformat(row['reminderDatetime'])  ,done=bool(row['done']),reminded=bool(row['reminded'])))
        return tasks
    

class Users:
     
    @staticmethod
    def __connect():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
       
        resources_dir = os.path.join(BASE_DIR, "resources")
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
            
        DB_PATH = os.path.join(resources_dir, "users.db")
        
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
    def addUser(username:str,password:str,email:str):
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
    def deleteUser(username:str):
        with Users.__connect() as conn:
            cursor = conn.execute("DELETE FROM users WHERE username = ?", (username,))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {username} not found.")

    @staticmethod
    def changePassword(username:str,password:str):
        ph=PasswordHasher()
        password=ph.hash(password)
        with Users.__connect() as conn:
            cursor = conn.execute("UPDATE users SET password = ? WHERE username = ?", (password,username))
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task ID {username} not found.")

    @staticmethod
    def changeEmail(username:str,email:str):
        with Users.__connect() as conn:
            cursor = conn.execute("UPDATE users SET email = ? WHERE username = ?", (email,username))
            if cursor.rowcount == 0:
                raise UserNotFound(f"{username} not found.")
    
    @staticmethod
    def account(username:str,password:str):
        with Users.__connect() as conn:
            ph=PasswordHasher()
            cursor=conn.execute("SELECT password FROM users WHERE username=?",(username,)).fetchone()
            if not cursor:
                raise UserNotFound("User Not Found")
            ph.verify(cursor[0],password)
            #return cursor
        

            
      

    