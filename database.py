import sqlite3
from errors import TaskAlreadyExists,TaskNotFound


class Database:
    connection=sqlite3.connect("todo_data.db")
    @staticmethod
    def addTask(task):
        connect=Database.connection
        read=connect.execute("SELECT * FROM todo WHERE task=?").fetchall()
        if not read:
           connect.execute("INSERT INTO todo(task) VALUES(?)",(task,))
           connect.commit()
        else:
            raise TaskAlreadyExists(f"{task} Already Exists")
          
    @staticmethod
    def deleteTask(task):
            connect=Database.connection
            read=connect.execute("SELECT * FROM todo WHERE task=?").fetchall()
            if read:
               connect.execute("DELETE FROM todo WHERE task = ?",(task,))
               connect.commit()
            else:
                raise TaskNotFound(f"{task} NOT Found")
            
    @staticmethod
    def toggleDone(task):
            connect=Database.connection
            read=connect.execute("SELECT * FROM todo WHERE task=?").fetchall()
            if read:
               connect.execute("UPDATE todo SET done = 1-done WHERE task = ?",(task,))
               connect.commit()
            else:
                raise TaskNotFound(f"{task} NOT Found")
           
                  
    
    