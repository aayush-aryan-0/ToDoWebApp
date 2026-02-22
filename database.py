import sqlite3
from errors import TaskAlreadyExists,TaskNotFound
from task import Task


class ToDoDB:
    
    @staticmethod
    def __connect():
        connect=sqlite3.connect("todo_data.db")
        connect.execute('''CREATE TABLE IF NOT EXISTS todo
                            (task TEXT PRIMARY KEY,
                            done INTEGER NOT NULL DEFAULT 0)''')
        return connect

    @staticmethod
    def addTask(task):
        connect=ToDoDB.__connect()
        read=connect.execute("SELECT * FROM todo WHERE task=?").fetchall()
        if not read:
           connect.execute("INSERT INTO todo(task) VALUES(?)",(task,))
           connect.commit()
        else:
            raise TaskAlreadyExists(f"{task} Already Exists")
          
    @staticmethod
    def deleteTask(task):
            connect=ToDoDB.__connect()
            read=connect.execute("SELECT * FROM todo WHERE task=?").fetchone()
            if read:
               connect.execute("DELETE FROM todo WHERE task = ?",(task,))
               connect.commit()
            else:
                raise TaskNotFound(f"{task} NOT Found")
            
    @staticmethod
    def toggleDone(task):
            connect=ToDoDB.__connect()
            read=connect.execute("SELECT * FROM todo WHERE task=?").fetchone()
            if read:
               connect.execute("UPDATE todo SET done = 1-done WHERE task = ?",(task,))
               connect.commit()
            else:
                raise TaskNotFound(f"{task} NOT Found")
            
    @staticmethod
    def readToDoDB():
        connect=ToDoDB.__connect()
        read=connect.execute("SELECT * FROM todo").fetchall()
        tasks=[]
        for row in read: 
            tasks.append(Task(row[0],row[1]==1))
        return tasks

    
           
                  
    
    