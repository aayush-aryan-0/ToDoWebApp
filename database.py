import sqlite3
import os
from errors import TaskAlreadyExists, TaskNotFound
from task import Task

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
                datetime TEXT DEFAULT (datetime('now', 'localtime')),
                done INTEGER NOT NULL DEFAULT 0
            )
        ''')
        return connect

    @staticmethod
    def addTask(task: Task):
        if not isinstance(task, Task):
            raise TypeError("task must be an object of class Task")
        
        with ToDoDB.__connect() as conn:
            cursor = conn.execute(
                "INSERT INTO todo(task, done) VALUES(?, ?)", 
                ((task.text), task.done)
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
                (task.text,task.datetime, task.done, task.id)
            )
            if cursor.rowcount == 0:
                raise TaskNotFound(f"Task {task.id} - {task.text} not found.")

    @staticmethod
    def readToDoDB():
        tasks = []
        with ToDoDB.__connect() as conn:
            cursor = conn.execute("SELECT * FROM todo")
            for row in cursor.fetchall():
                tasks.append(Task(id=row['id'],text=row['task'], datetime=row['datetime'] ,done=bool(row['done'])))
        return tasks