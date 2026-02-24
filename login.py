from flask import Blueprint, render_template, request, redirect, url_for, session,Flask
from task import Task
from database import *
from datetime import datetime
app=Flask(__name__)


login_bp = Blueprint('login', __name__)  

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')
        account=Users.account(username,password)
        if account:
             session['loggedin'] = True
             session['username'] = account['username']
             return redirect(url_for('home')) 
        else:
            return render_template('login.html',message='Invalid Username/Password')
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login.login'))

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Users.addUser(username,password,email)
        return render_template('register.html')
    else:
        return render_template('register.html',mssg='Something went wrong')