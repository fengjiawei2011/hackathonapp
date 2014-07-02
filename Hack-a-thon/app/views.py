'''
Created on Jul 2, 2014

@author: lan_xu
'''
from app import app, lm, sqldb
from models import User
from forms import LoginForm, RegisterForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from datetime import datetime, date, time, timedelta

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(request.args.get('next') or url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('home'))
        else:
            form.password.errors.append('Invalid Crednetials')
            flash('Invalid login. Please try again.')

    return render_template("login.html",
                           form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    # TODO 
    #===========================================================================
    # if g.user is not None and g.user.is_authenticated():
    #     return redirect(request.args.get('next') or url_for('home'))
    #===========================================================================
    def add_user(name, pwd):
        user = User(username=name, password=pwd)
        sqldb.session.add(user)
        sqldb.session.commit()
    form = RegisterForm()
    if form.validate_on_submit():
        add_user(form.username.data, form.password.data)
        flash('OKAY')
#         user = User.query.filter_by(username = form.username.data).first()
#         if user is not None and user.check_password(form.password.data):
#             login_user(user)
#             return redirect(request.args.get('next') or url_for('home'))
#         else:
#             form.password.errors.append('Invalid Crednetials')
#             flash('Invalid login. Please try again.')    
    return render_template("register.html", form = form)