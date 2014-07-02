'''
Created on Jul 2, 2014

@author: lan_xu
'''
from app import app, lm, sqldb
from models import User, Event, Team, Member
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
        return redirect(request.args.get('next') or url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            print("login");
            return redirect(request.args.get('next') or url_for('dashboard'))
        else:
            form.password.errors.append('Invalid Crednetials')
            flash('Invalid login. Please try again.')

    return render_template("login.html",
                           form = form)


@app.route('/event/<int:event_id>/team', methods = ['GET', 'POST'])
@login_required
def add_team(event_id):
    if request.method == 'POST':
        user = g.user
        team = Team(user_id = user.id, event_id = event_id, name = request.form.get('name'))
        sqldb.session.add(team)
        sqldb.session.commit()
        
        members = request.form.getlist('member')
        for m in members:
            member = Member(team_id = team.id, member_name = m)
            sqldb.session.add(member)
        
        sqldb.session.commit()
        
        return request.form.get('name') + ' is  added.'
    return render_template("team.html")


@app.route('/')
@login_required
def dashboard():
    user = g.user
    return user.username + "Welcome to dashboard"
    
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('dashboard'))
    def add_user(first_name, last_name, username, pwd):
        user = User(first_name=first_name, last_name=last_name, username=username, password=pwd)
        sqldb.session.add(user)
        sqldb.session.commit()
    form = RegisterForm()
    if form.validate_on_submit():
        add_user(form.first_name.data, form.last_name.data, form.username.data, form.password.data)
        flash('OKAY')
    return render_template("register.html", form = form)
