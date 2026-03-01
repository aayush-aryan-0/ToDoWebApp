from flask import Flask, render_template, redirect, url_for, session,request
from login import login_bp  
from database import ToDoDB
from task import Task
from datetime import datetime
from threading import Thread
from reminder import reminder
app=Flask(__name__)
app.secret_key = "supersecret"  
app.register_blueprint(login_bp)
mssg=""
Thread(target=reminder,daemon=True).start()
@app.route('/')
def home():
    if not session.get('loggedin'):
        return redirect(url_for('login.login'))
    taskList=ToDoDB.readToDoDB()
    tasks=[[]]
    for task in taskList:
        tasks.append([task.id,task.text,task.datetime,task.done])
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return render_template('index.html',mindatetime=now_str,tasks=taskList,message=mssg)

@app.route("/add",methods=['POST'])
def add():
    try:
        ToDoDB.addTask(Task(""))
    except Exception as e:
        mssg=e
        return redirect('/') 
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
        mssg=e
        return redirect('/') 
    else:
        return redirect('/') 
    
@app.route("/delete",methods=['POST'])
def delete():
    try:
        id=request.form.get("id")
        ToDoDB.deleteTask(Task(id=id))
    
    except Exception as e:
        mssg=e
        return redirect('/') 
    else:
        return redirect('/') 



if __name__ == "__main__":
    app.run(port=50001,debug=True)