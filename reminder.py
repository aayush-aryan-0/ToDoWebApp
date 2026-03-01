from telegramAPI import sendBot
from database import ToDoDB

from time import sleep
from datetime import datetime
def reminder():
    while True:
        curr_time=datetime.now()
       
        todoList=ToDoDB.readToDoDB()
        for task in todoList:
            task.datetime.replace("T"," ")
            if (curr_time<=datetime.strptime(task.datetime, '%Y-%m-%dT%H:%M:%S')) and (not task.done) and (not task.reminded):
                reminderTimeStr=task.datetime.replace("T"," ")
                reminderTime=datetime.strptime(reminderTimeStr, "%Y-%m-%d %H:%M:%S")
                reminderTimeStr=reminderTime.strftime("%d/%m/%Y %I:%M %p")

                sendBot(f"{task.text} your time is up {reminderTimeStr}")
                ToDoDB.toggleReminded(task)
        sleep(1)


