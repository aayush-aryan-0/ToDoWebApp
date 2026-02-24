from flask import Flask, render_template, request, redirect, url_for
from task import Task
from database import *

app=Flask(__name__)


@app.route('/')
@app.route('/<mssg>')
def home(mssg=None):
    taskList=ToDoDB.readToDoDB()
    tasks=[[]]
    for task in taskList:
        tasks.append([task.id,task.text,task.done])
    
    return render_template('index.html',tasks=taskList,message=mssg,TaskMessage=tasks)

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
    done=0
    if(check):
        done=1
    else:
        done=0  
    try:
        ToDoDB.updateTask(Task(text=text, id=id, done=done))
    
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