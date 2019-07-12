from flask import Flask, render_template, g, request, url_for, redirect, flash, session, logging
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import subprocess
import dbsys #class containing initializing/creating of db
import buz

#Threads
from threading import *
from scheduler import *

app = Flask(__name__)

database = "//home//pi//Documents//LIGHTS//db//sample.db"
		
app.database = database

class app_run(Thread):

	def run(self):
		
		global app
		
		@app.route('/')
		def index():
		
		    return render_template('home.html')
		
		def connect_db():
		    return sqlite3.connect(app.database)
		
		@app.route('/about')
		def about():
		    return render_template('about.html')
		
		@app.route('/manage')
		@login_required
		def manage():
		    return render_template('ad_main.html')
		
		@app.route('/ad_addEvent', methods = ["GET", "POST"])
		def add():
		    result=""
		    g.db = connect_db()
		    flash("working")
		    if request.method =="POST":
		
		        newEventName = request.form['eventname']
		        newEventTime = request.form['RingTime'] + ":00"
		        newEventDay = request.form.getlist('day')
		        count =0
		
		        if newEventDay ==[]:
		            result = "Oops, you forgot to tick the day(s) for this event"
		        else:
		            for day in newEventDay:
		                cur=g.db.execute("INSERT INTO Schedules (EventDay,EventName, RingTime) VALUES (?,?,?)",(day, newEventName, newEventTime))
		                g.db.commit()
		                result=" Event(s) Succefully Created."
		            g.db.close()
		            return render_template('ad_addEvent.html', result=result)
		            #else:
		            #    return render_template('ad_addEvent.html', result=result)
		        return render_template('ad_addEvent.html', result=result)
		    return render_template('ad_addEvent.html', result=result)
		
		@app.route('/articles')
		def articles():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT * FROM posts')
		    posts=[dict(title=row[0], description=row[1]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('articles.html', posts=posts)
		
		#Login
		# config
		app.config.update(
		    DEBUG = True,
		    SECRET_KEY = 'os.urandom(24) \xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
		)
		
		login_manager = LoginManager()
		login_manager.init_app(app)
		login_manager.login_view = "login"
		
		
		# silly user model
		class User(UserMixin):
		
		    def __init__(self, id):
		        self.id = id
		        self.name = "user" + str(id)
		        self.password = self.name + "_secret"
		
		    def __repr__(self):
		        return "%d/%s/%s" % (self.id, self.name, self.password)
		
		
		# create some users with ids 1 to 20
		users = [User(id) for id in range(1, 21)]
		
		
		@app.route('/login', methods = ["GET", "POST"])
		def login():
		    error = ''
		    try:
		        if request.method =="POST":
		            attempted_username= request.form['username']
		            attempted_password= request.form['password']
		
		
		            if attempted_username == "admin" and attempted_password == "admin":
		                app.logger.info(attempted_username)
		                app.logger.info(attempted_password)
		                error = "Login Successful."
		                user= User(id)
		                login_user(user)
		                #return redirect(url_for('ad_main'))
		                return render_template('/ad_main.html')
		            else:
		                error = "Invalid login details. Please try again."                
		        return render_template('/login.html', error = error )
		
		    except Exception as e:
		        return render_template('/login.html', error = error )
		
		@app.route('/Monday')
		def monday():
		        g.db = connect_db()
		        cur = g.db.execute('SELECT EventName, RingTime FROM Schedules WHERE EventDay=\"Monday\" ORDER BY RingTime ASC')
		        events=[dict(EventName=row[0], RingTime=row[1]) for row in cur.fetchall()]
		        g.db.close()
		        return render_template('monday.html', events=events)
		
		@app.route('/Tuesday')
		def Tuesday():
		        g.db = connect_db()
		        cur = g.db.execute('SELECT EventName, RingTime FROM Schedules WHERE EventDay=\"Tuesday\" ORDER BY RingTime ASC')
		        events=[dict(EventName=row[0], RingTime=row[1]) for row in cur.fetchall()]
		        g.db.close()
		        return render_template('tuesday.html', events=events)
		
		@app.route('/Wednesday')
		def Wednesday():
		        g.db = connect_db()
		        cur = g.db.execute('SELECT EventName, RingTime FROM Schedules WHERE EventDay=\"Wednesday\" ORDER BY RingTime ASC')
		        events=[dict(EventName=row[0], RingTime=row[1]) for row in cur.fetchall()]
		        g.db.close()
		        return render_template('wednesday.html', events=events)
		
		@app.route('/Thursday')
		def Thursday():
		        g.db = connect_db()
		        cur = g.db.execute('SELECT EventName, RingTime FROM Schedules WHERE EventDay=\"Thursday\" ORDER BY RingTime ASC')
		        events=[dict(EventName=row[0], RingTime=row[1]) for row in cur.fetchall()]
		        g.db.close()
		        return render_template('thursday.html', events=events)
		
		@app.route('/Friday')
		
		def Friday():
		        g.db = connect_db()
		        cur = g.db.execute('SELECT EventName, RingTime FROM Schedules WHERE EventDay=\"Friday\" ORDER BY RingTime ASC')
		        events=[dict(EventName=row[0], RingTime=row[1]) for row in cur.fetchall()]
		        g.db.close()
		        return render_template('friday.html', events=events)
		
		#Admin Home page
		@app.route('/ad_main')
		@login_required
		def ad_home():
		    return render_template('ad_main.html')
		
		#Edit Monday Times
		@app.route('/ad_monday', methods =['GET', 'POST'])
		@login_required
		def editMonday():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT EventID, EventName, RingTime FROM Schedules WHERE EventDay=\"Monday\" ORDER BY RingTime ASC')
		    events=[dict(EventID=row[0], EventName=row[1], RingTime=row[2]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('ad_monday.html', events=events)
		
		
		#Call to ring the bell
		@app.route('/ad_ringnow')
		@login_required
		def ringNow():
		    #process = subprocess.Popen(['python' , '/home/pi/Bell/buz.py' ])
		    #out, err = process.communicate()
		    #print(out)
		    buz.blink()
		    print("LED has just blinked!")
		    return render_template('ad_main.html')
		
		@app.route('/ad_editEvent')
		@login_required
		def editMonEvent():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_editEvent.html', edit=edit)
		
		
		@app.route('/ad_tuesday', methods =['GET', 'POST'])
		@login_required
		def editTuesday():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT EventID, EventName, RingTime FROM Schedules WHERE EventDay=\"Tuesday\" ORDER BY RingTime ASC')
		    events=[dict(EventID=row[0], EventName=row[1], RingTime=row[2]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('ad_tuesday.html', events=events)
		
		
		@app.route('/ad_editEvent')
		@login_required
		def editTueEvent():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_editEvent.html', edit=edit)
		
		#Edit Wednesday times
		@app.route('/ad_wednesday', methods =['GET', 'POST'])
		@login_required
		def editWednesday():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT EventID, EventName, RingTime FROM Schedules WHERE EventDay=\"Wednesday\" ORDER BY RingTime ASC')
		    events=[dict(EventID=row[0], EventName=row[1], RingTime=row[2]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('ad_wednesday.html', events=events)
		
		
		@app.route('/ad_editEvent')
		def editWedEvent():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_editEvent.html', edit=edit)
		
		#Edit Thursday times
		@app.route('/ad_thursday', methods =['GET', 'POST'])
		@login_required
		def editThursday():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT EventID, EventName, RingTime FROM Schedules WHERE EventDay=\"Thursday\" ORDER BY RingTime ASC')
		    events=[dict(EventID=row[0], EventName=row[1], RingTime=row[2]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('ad_thursday.html', events=events)
		
		
		@app.route('/ad_editEvent')
		@login_required
		def edit():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_editEvent.html', edit=edit)
		
		#Edit Friday Times
		@app.route('/ad_friday', methods =['GET', 'POST'])
		@login_required
		def editFriday():
		    g.db = connect_db()
		    cur = g.db.execute('SELECT EventID, EventName, RingTime FROM Schedules WHERE EventDay=\"Friday\" ORDER BY RingTime ASC')
		    events=[dict(EventID=row[0], EventName=row[1], RingTime=row[2]) for row in cur.fetchall()]
		    g.db.close()
		    return render_template('ad_friday.html', events=events)
		
		
		@app.route('/ad_editEvent')
		@login_required
		def editFriEvent():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_main.html', edit=edit)
		
		#Update time. Called by all the respective ad_XXXX modules
		@app.route('/update')
		@login_required
		def update():
		    id= request.args.get('eventID')
		    updateName = request.args.get('EventName')
		    updateRingTime = request.args.get('RingTime')
		
		    g.db = connect_db()
		    cur = g.db.execute("UPDATE Schedules SET EventName=?, RingTime=? WHERE EventID=?", (updateName, updateRingTime, id))
		    g.db.commit()
		    g.db.close()
		    return render_template('ad_editEvent.html', edit=edit)
		
		#Delete time. Called by all the respective ad_XXXX modules
		@app.route('/ad_deleteEvent')
		@login_required
		def confirmdelete():
		    id= request.args.get('id')
		
		    g.db = connect_db()
		    cur = g.db.execute("SELECT EventID, EventName, RingTime FROM Schedules WHERE EventID=?", [id])
		    result=cur.fetchall()
		    edit=result[0]
		    g.db.close()
		    return render_template('ad_deleteEvent.html', edit=edit)
		
		@app.route('/delete')
		def delete():
		    id= request.args.get('eventID')
		    g.db = connect_db()
		    cur = g.db.execute("DELETE FROM Schedules WHERE EventID=?", [id])
		    g.db.commit()
		    g.db.close()
		    msg ="Event Removed"
		    return render_template('ad_main.html', msg=msg)
		
		# callback to reload the user object
		@login_manager.user_loader
		def load_user(userid):
		    return User(userid)
		
		@app.route("/logout")
		@login_required
		def logout():
		    logout_user()
		    return render_template('home.html')
		
		
if __name__=='__main__':
	app.secret_key ='\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
	app.run(host='0.0.0.0',port=80,debug=True)

thread_scheduler = Scheduler()
thread_app_run = app_run()

thread_scheduler.start()
thread_app_run.start()


