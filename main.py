from flask import Flask, flash, render_template, redirect, url_for, session,request
from login import login_bp  
from database import ToDoDB
from task import Task
from datetime import datetime
from threading import Thread
from reminder import reminder
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(login_bp)


@app.route('/')
def home():
    if not session.get('loggedin'):
        return redirect(url_for('login.login'))
    taskList=ToDoDB.readToDoDB()
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return render_template('index.html',mindatetime=now_str,tasks=taskList)

@app.route("/add",methods=['POST'])
def add():
    try:
        ToDoDB.addTask(Task(""))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home')) 
    else:
        return redirect(url_for('home')) 

@app.route("/save",methods=['POST'])
def save():
    id=request.form.get("id")
    text = request.form.get("text")
    check = request.form.get("done")
    taskDatetime=request.form.get("datetime")
    done= 1 if check else 0 

    try:
        ToDoDB.updateTask(Task(text=text, id=id, done=done,datetime=taskDatetime))
    
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home'))  
    else:
        return redirect(url_for('home'))  
    
@app.route("/delete",methods=['POST'])
def delete():
    try:
        id=request.form.get("id")
        ToDoDB.deleteTask(Task(id=id))
    
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home')) 
    else:
        return redirect(url_for('home')) 



if __name__ == "__main__":
    Thread(target=reminder,daemon=True).start()
    app.run(port=50001,debug=True)