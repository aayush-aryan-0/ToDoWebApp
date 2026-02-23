from flask import Flask, render_template, request, redirect, url_for
from task import Task
from database import *

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html',tasks=ToDoDB.readToDoDB())

@app.route("/add",methods=['POST'])
def add():
    try:
        ToDoDB.addTask("",0)
    except Exception as e:
        print(e)
    return redirect('/')

@app.route("/save",methods=['POST'])
def save():
    try:
        text=text = request.form.get("text")
        done=text = request.form.get("done")

        if(done):
            ToDoDB.addTask(text,1)
        else:
            ToDoDB.addTask(text,0)
    except Exception as e:
        print(e)
    return redirect('/') 
    
@app.route("/delete",methods=['POST'])
def delete():
    try:
        text=text = request.form.get("text")
        ToDoDB.deleteTask(text)
    except Exception as e:
        print(e)
    return redirect('/') 



if __name__ == "__main__":
    app.run(port=50001,debug=True)