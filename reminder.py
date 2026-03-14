from telegramAPI import sendBot
from database import ToDoDB
from task import Task
from time import sleep
from datetime import datetime
def reminder():
    while True:
        curr_time=datetime.now()
       
        todoList:Task=ToDoDB.readToDoDB()
        for task in todoList:
            if (curr_time<=task.reminderDatetime) and (not task.done) and (not task.reminded):
                reminderTimeStr=(task.reminderDatetime).strftime("%d/%m/%Y %I:%M %p")
                print(reminderTimeStr)
                sendBot(f"{task.text} your time is up {reminderTimeStr}")
                ToDoDB.toggleReminded(task)
        sleep(1)


