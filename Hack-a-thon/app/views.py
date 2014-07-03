'''
Created on Jul 2, 2014

@author: lan_xu, alvin_yau
'''
from app import app, lm, sqldb
from models import User, Event, Team, Member
from forms import LoginForm, RegisterForm, EventForm, TeamForm
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
            return redirect(request.args.get('next') or url_for('dashboard'))
        else:
            form.password.errors.append('Invalid Crednetials')
            flash('Invalid login. Please try again.')

    return render_template("login.html",
                           form = form)


@app.route('/event/<int:event_id>/team', methods = ['GET', 'POST'])
@login_required
def add_team(event_id):
    event = Event.query.get(event_id)
    teamform = TeamForm()
    if event.teams.count() >= event.max_team:
        flash('Sorry, no more space available.')
        return redirect(url_for('event', event_id = event_id))
    
    elif teamform.validate_on_submit():
        user = g.user
        team = Team(user_id = user.id, event_id = event_id, name = request.form.get('teamname'))
        sqldb.session.add(team)
        sqldb.session.commit()
        
        members = request.form.getlist('member')
        for m in members:
            if m!="":
                member = Member(team_id = team.id, member_name = m)
                sqldb.session.add(member)
        
        sqldb.session.commit()
        
        return redirect(url_for('event', event_id = event_id))
    return render_template("team.html",
                           team = None,
                           form = teamform,
                           n = event.max_member_per_team)


@app.route('/team/<int:team_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_team(team_id):
    team = Team.query.get(team_id)
    user = g.user
    teamform = TeamForm()
    
    if user.id != team.user_id:
        flash('Only the team creator can update the team information.')
        
    elif teamform.validate_on_submit():       
        team.name = request.form.get('teamname')
        
        for m in team.members:
            sqldb.session.delete(m)
            
        members = request.form.getlist('member')
        for m in members:
            if m!="":
                member = Member(team_id = team.id, member_name = m)
                sqldb.session.add(member)
        
        sqldb.session.commit()
        
        return redirect(url_for('event', event_id = team.event.id))
    
    return render_template("team.html",
                           team = team,
                           form = teamform,
                           n = team.event.max_member_per_team)
    
@app.route('/team/<int:team_id>', methods = ['GET', 'POST'])
@login_required
def team(team_id):
    team = Team.query.get(team_id)
    event_id = team.event.id
    user = g.user
    
    if user.id != team.user_id:
        flash('Only the team creator can delete/edit the team.')
        
    elif request.method == 'POST':
        for m in team.members:
            sqldb.session.delete(m)
        sqldb.session.delete(team)
        sqldb.session.commit()
        return redirect(url_for('event', event_id = event_id))
        
    return render_template("team_view.html",
                           team = team)
    
       
@app.route('/', methods = ['GET', 'POST'])
@app.route('/<int:page>', methods = ['GET', 'POST'])
@login_required
def dashboard(page=1):
    user = g.user
    events = Event.query.order_by(Event.starttime.desc()).paginate(page, 5, False)
    return render_template("dashboard.html",
                           events = events,
                           user = user)
    
    
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


@app.route('/createEvent', methods = ['GET', 'POST'])
@login_required
def create_event():
    user = g.user
    if not user.is_admin():
        return redirect(url_for('dashboard')) 
    form = EventForm()
    event = Event() 
    if form.validate_on_submit():
        event = Event(user_id = user.id, name = request.form.get('name'), description = request.form.get('description'), starttime = request.form.get('starttime'), endtime = request.form.get('endtime'), location = request.form.get('location'), max_team = request.form.get('max_team'), max_member_per_team = request.form.get('max_member_per_team'), department = request.form.get('department'))
        sqldb.session.add(event)
        sqldb.session.commit()
        return redirect(url_for('event', event_id = event.id))
    return render_template("event.html", form = form, event = event)

#==============================================================================
# @author alvin_yau
# Render Edit Event Page with an event from the event object 
#==============================================================================
@app.route('/event/<int:event_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_event(event_id):
    user = g.user
    form = EventForm()
    print(event_id)
    event = Event.query.get(event_id)
    #assert event != null, "SHIT"
    if not user.is_admin():
        if user.id != event.user_id:
            return redirect(url_for('dashboard'))
        
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.starttime = form.starttime.data
        event.endtime = form.endtime.data
        event.max_team = form.max_team.data
        event.max_member_per_team = form.max_member_per_team.data
        event.department = form.department.data
        sqldb.session.commit()
        return redirect(url_for('event', event_id = event_id))
    if event == None:
        # TODO NOT WORKING
        print("Event not found!")
       
    return render_template("edit_event.html", event = event, form = form)


@app.route('/event/<int:event_id>', methods = ['GET', 'POST'])
@login_required
def event(event_id):
    event = Event.query.get(event_id)
    user = g.user
        
    if request.method == 'POST':
        if not user.is_admin():
            return redirect(url_for('dashboard'))
        
        for team in event.teams:          
            for m in team.members:
                sqldb.session.delete(m)             
            sqldb.session.delete(team)            
        sqldb.session.delete(event)
        
        sqldb.session.commit()
        return redirect(url_for('dashboard'))
        
    return render_template("event_view.html",
                           user = user,
                           event = event)



