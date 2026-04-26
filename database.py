from errors import *
from task import Task
from datetime import datetime
from argon2 import PasswordHasher
from dateformate import isHtmlFormat,isSqlFormat
import psycopg2

class Connection:
    
    @staticmethod
    def connect()->psycopg2.extensions.connection:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="kiit",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY ,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS todo (
                id SERIAL PRIMARY KEY ,
                task_text TEXT DEFAULT '',
                reminderDatetime TIMESTAMP DEFAULT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE,
                reminded BOOLEAN NOT NULL DEFAULT FALSE,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        cur.close()
        return conn


class ToDoDB:
    

    @staticmethod
    def addTask(username:str)->None:
        
        with Connection.connect() as conn:
            cur=conn.cursor()
            cur.execute(
                "INSERT INTO todo(user_id) VALUES(%s) RETURNING id", 
                (Users.getUserId(username),)
            )
            if cur.fetchone() is None:
                raise TaskNotFound(f"Something went wrong cannot add Task")
           

    @staticmethod
    def deleteTask(id:int)->None:
        with Connection.connect() as conn:
            cur=conn.cursor()
            cur.execute("DELETE FROM todo WHERE id = %s RETURNING id", (id,))
            if cur.fetchone() is None:
                raise TaskNotFound(f"Task {id} not found.")

    @staticmethod
    def toggleDone(id:int)->None:
        with Connection.connect()  as conn:
            cur=conn.cursor()
            cur.execute("UPDATE todo SET done = NOT done WHERE id = %s RETURNING id", (id,))
            if cur.fetchone() is None:
                raise TaskNotFound(f"Task ID {id} not found.")

    @staticmethod
    def updateTask(id:int, text:str,done:bool,reminderDatetime:datetime)->None:
        with Connection.connect()  as conn:
            cur=conn.cursor()
            cur.execute(
                    "UPDATE todo SET task_text  = COALESCE(%s,task_text), reminderDatetime = COALESCE(%s, reminderDatetime) , done = %s WHERE id = %s RETURNING id",
                    (text,reminderDatetime,done,id))
            
            if cur.fetchone() is None:
                raise TaskNotFound(f"Task {text} not found.")

    @staticmethod
    def toggleReminded(id:int)->None:
        with Connection.connect()  as conn:
            cur=conn.cursor()
            cur.execute(
                "UPDATE todo SET reminded = NOT reminded WHERE id = %s RETURNING id",
                (id,)
            )
            if cur.fetchone() is None:
                raise TaskNotFound(f"Task id {id} not found.")
    

    @staticmethod
    def readToDoDB(username:str)->list:
        tasks = []
        with Connection.connect()  as conn:
            cur=conn.cursor()
            cur.execute("SELECT * FROM todo where user_id =%s",(Users.getUserId(username),))
            for row in cur.fetchall():
                if row[2]:
                    reminderDateTime=row[2].strftime("%Y-%m-%dT%H:%M")
                else:
                    reminderDateTime=None
                tasks.append(Task(id=row[0],text=row[1], reminderDatetime=reminderDateTime,done=(row[3]),reminded=bool(row[4])))
        return tasks
    
    @staticmethod
    def readAllToDoDB()->list:
        tasks = []
        with Connection.connect()  as conn:
            cur=conn.cursor()
            cur.execute("SELECT * FROM todo ")
            for row in cur.fetchall():
                tasks.append(Task(id=row[0],text=row[1], reminderDatetime=row[2],done=(row[3]),reminded=bool(row[4])))
        return tasks
    

class Users:

    @staticmethod
    def getUserId(username:str)->int:
        with Connection.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users where username=%s",(username,))
                user_id:int=cur.fetchone()[0]
                return user_id
     
    @staticmethod
    def addUser(username:str,password:str,email:str)->None:
       
            ph=PasswordHasher()
            password=ph.hash(password)
            with Connection.connect()  as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(
                            "INSERT INTO users(username, password,email) VALUES(%s, %s,%s)", 
                            (username,password,email)
                        )
                    except psycopg2.errors.UniqueViolation:
                        raise UserAlreadyExists


    @staticmethod
    def deleteUser(username:str)->None:
        with Connection.connect()  as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE username = %s RETURNING id", (username,))
                row=cursor.fetchone()
                Users.checkUserExists(row,username)

    @staticmethod
    def changePassword(username:str,password:str)->None:
        ph=PasswordHasher()
        password=ph.hash(password)
        with Connection.connect()  as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s RETURNING id", (password,username))
                row=cursor.fetchone()
                Users.checkUserExists(row,username)

    @staticmethod
    def changeEmail(username:str,email:str)->None:
        with Connection.connect()  as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET email = %s WHERE username = %s RETURNING id", (email,username))
                row=cursor.fetchone()
                Users.checkUserExists(row,username)

                
    
    @staticmethod
    def account(username:str,password:str)->None:
        with Connection.connect() as conn:
            with conn.cursor() as cursor:
                ph=PasswordHasher()
                cursor.execute("SELECT password FROM users WHERE username=%s",(username,))
                row=cursor.fetchone()
                if not row:
                    raise UserNotFound("User Not Found")
                ph.verify(row[0],password)
    @staticmethod
    def checkUserExists(row:tuple,username:str)->None:
        if row is None:
                    raise UserNotFound(f"{username} not found.")
        

            
      

    