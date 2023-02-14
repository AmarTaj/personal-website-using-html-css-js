# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()
styleDict = {'owner@email.com': 'width: 100%;color:blue;text-align: right', 'guest@email.com': 'width: 100%;color:grey;text-align: left'}


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    auth = db.authenticate(email=form_fields['email'], password=form_fields['password'])
    if auth['success'] == 1:
        session['email'] = form_fields['email']
        return json.dumps({'success': 1})
    return json.dumps({'success':0})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
	join_room('main')
	emit('status', {'msg': getUser() + ' has entered the room.', 'style': styleDict[getUser()], 'user': getUser()}, room='main')

@socketio.on('leaveChat', namespace='/chat')
def leave(message):
	print("message received to python side!")
	emit('leave', {'msg': getUser() + ' has left the room.', 'style': styleDict[getUser()]}, room='main')
	leave_room('main')
	

@socketio.on('sendMessage', namespace='/chat')
def sendMessage(message):
	print("trying to send message - reached part of python for 'sendMessage!!! ")
	print(message)
	print("above is the received message! lol ")
	emit('messageToChat', {'msg': message, 'style': styleDict[getUser()]}, room ='main')


#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	print(db.query('SELECT * FROM users'))
	x = random.choice(['I can speak 11 languages.','I am learning 2D animation.','I love elephants.'])
	return render_template('home.html', user=getUser(), fun_fact = x)

# Resume page
@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

# Post resume update
@app.route('/processresume', methods = ['POST'])
def processresume():
	resumeNew = request.form
	user = getUser()
	if resumeNew and user[0:5]=="owner":
		name, title, city, state, desc, start, end, resp, respdesc = resumeNew["instname"], resumeNew["jobtitle"], resumeNew["city"], resumeNew["state"], resumeNew["desc"], resumeNew["start"], resumeNew["end"], resumeNew["resp"],resumeNew["respdesc"]
		db.insertRows("institutions", ["type","name","city","state"], [["academia",name,city,state]])
		line = db.query("SELECT MAX(inst_id) FROM institutions;")
		id_ = line[0]['MAX(inst_id)']
		db.insertRows("positions", ["inst_id","title","responsibilities","start_date","end_date"], [[id_,title,desc,start,end]])
		line = db.query("SELECT MAX(position_id) FROM positions;")
		id_ = line[0]['MAX(position_id)']
		db.insertRows("experiences", ["position_id","name","description","hyperlink","start_date","end_date"], [[id_,resp,respdesc,"NULL",start,end]])
	return redirect("/resume")

# Post resume edit
@app.route('/processresumeedit', methods = ['POST'])
def processresumeedit():
	resumeEdit = request.form
	user = getUser()
	if resumeEdit and user[0:5]=="owner":
		from__, to__ = resumeEdit["from"], resumeEdit["to"]
		what = resumeEdit["change"]
		what = what.split()
		line = db.query(f'UPDATE {what[0]}\nSET {what[1]} = "{to__}"\nWHERE {what[1]}="{from__}";')
	return redirect("/resume")

# Projects page
@app.route('/projects')
def projects():
	return render_template('projects.html')

# Piano page
@app.route('/piano')
def piano():
	return render_template('piano.html')

# Post-feedback page
@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	if feedback:
		name, email, comment = feedback["name"], feedback["email"], feedback["comment"]
		db.insertRows("feedback", ["name","email","comment"], [[name,email,comment]])
	data = db.query("SELECT DISTINCT * FROM feedback;")
	return render_template('feedback.html', data=data)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
