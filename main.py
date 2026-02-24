from flask import Flask, render_template, request, redirect, url_for
from task import Task
from database import *
from datetime import datetime
app=Flask(__name__)


@app.route('/')
@app.route('/<mssg>')
def home(mssg=None):
    taskList=ToDoDB.readToDoDB()
    tasks=[[]]
    for task in taskList:
        tasks.append([task.id,task.text,task.datetime,task.done])
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template('index.html',mindatetime=now_str,tasks=taskList,message=mssg,TaskMessage=tasks)

@app.route("/add",methods=['POST'])
def add():
    try:
        ToDoDB.addTask(Task(""))
    except Exception as e:
        return redirect(f'/{e}')
    else:
        return redirect('/')

@app.route("/save",methods=['POST'])
def save():
    id=request.form.get("id")
    text = request.form.get("text")
    check = request.form.get("done")
    datetime=request.form.get("datetime")

    done=0
    if(check):
        done=1
    else:
        done=0  
    try:
        ToDoDB.updateTask(Task(text=text, id=id, done=done,datetime=datetime))
    
    except Exception as e:
        return redirect(f'/{e} also {text} also {done}')
    else:
        return redirect(f'/also {text} also {done}') 
    
@app.route("/delete",methods=['POST'])
def delete():
    try:
        id=request.form.get("id")
        ToDoDB.deleteTask(Task(id=id))
    
    except Exception as e:
        return redirect(f'/{e}')
    else:
        return redirect('/') 



if __name__ == "__main__":
    app.run(port=50001,debug=True)