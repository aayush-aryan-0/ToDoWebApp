from flask import Flask, flash, render_template, redirect, url_for, session,request
from login import login_bp  
from database import ToDoDB
from task import Task
from datetime import datetime
import workerMain
from dotenv import load_dotenv
from dateformate import isHtmlFormat,isSqlFormat
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(login_bp)


@app.route('/')
def home():
    if not session.get('loggedin'):
        return redirect(url_for('login.login'))
    taskList=ToDoDB.readToDoDB(session.get('username'))
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template('index.html',mindatetime=now_str,tasks=taskList)

@app.route("/add",methods=['POST'])
def add():
    try:
        ToDoDB.addTask(session.get('username'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home')) 
    else:
        return redirect(url_for('home')) 

@app.route("/save",methods=['POST'])
def save():
    try:
        ToDoDB.updateTask(id=request.form.get("id"), text=request.form.get("text"),done=bool(request.form.get("done")) ,reminderDatetime=(request.form.get("reminderDatetime") or None))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home'))  
    else:
        return redirect(url_for('home'))  
    
@app.route("/delete",methods=['POST'])
def delete():
    try:
        id=request.form.get("id")
        ToDoDB.deleteTask(id)
    
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home')) 
    else:
        return redirect(url_for('home')) 



if __name__ == "__main__":
    workerMain.Thread()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port,debug=True)