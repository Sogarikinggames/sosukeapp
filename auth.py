from flask import Blueprint, render_template, request, redirect, flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pass = generate_password_hash(password)

        email_exits = User.query.filter_by(username=username).first()
        if email_exits:
            flash('Username already exit',category='error')
        elif len(username) < 2:
            flash('Username is too short',category='error')
        elif len(password) < 6:
            flash('Password is too short',category='error')
        else:
            new_user = User(username=username, password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            flash('You are now registered',category='success')
            return redirect('/login')

    elif request.method == 'GET':
        return render_template('signup.html',user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password=password):
            flash('You are now logged in',category='success')
            login_user(user,remember=True)
            return redirect('/admin')
        else:
            flash('Invalid username or password',category='error')
            return redirect('/login')
    elif request.method == 'GET':
        return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
