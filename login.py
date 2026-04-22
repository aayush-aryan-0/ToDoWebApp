from flask import Blueprint, render_template, request, redirect, url_for, session,Flask,flash
from task import Task
from database import *
from errors import *
from datetime import datetime



login_bp = Blueprint('login', __name__)  

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')
        try:
            Users.account(username,password)
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('home')) 
        except UserNotFound as e:
            flash(str(e))
            return render_template('login.html')
        except PasswordMismatchError as e:
            flash(str(e))
            return render_template('login.html')
        except Exception as e:
            flash(str(e))
            return render_template('login.html') 
        
        
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    try:
        session.pop('loggedin', None)
        session.pop('username', None)
        return redirect(url_for('login.login'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home'))


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            Users.addUser(username,password,email)
            return render_template('login.html')
        else:
            flash("Something went wrong")
            return render_template('register.html')
    except Exception as e:
        flash(str(e))
        return render_template('register.html')