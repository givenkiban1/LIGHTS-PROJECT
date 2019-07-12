import datetime
import time
import os
import sqlite3
from dbsys import *

command = 'python /home/pi/Documents/LIGHTS/buz.py'

conn = create_connection(database)
cur = conn.cursor()


#Continue to loop through the program every second
while 1 and (conn is not None):

    #Define day and time in loop so it alwats fetches current day and time.
    now= datetime.datetime.now()
    DayOfWeek = now.strftime("%A")
    CurrentTime = now.strftime("%H:%M:%S")

    #Get ring times for the current day.
    cur.execute("SELECT time(RingTime) FROM Schedules WHERE EventDay = ?", [DayOfWeek])
    #RingTimes=cur.fetchall()
    RingTimes=[(row[0]) for row in cur.fetchall()]

    #Search through the array and ring bell when array times match current time to the second
    for t in RingTimes:
        if t==str(CurrentTime):
            os.system(command)
            print ("The current time is: ", CurrentTime)
            print ("Times Match. BELL RINGS @....", CurrentTime)
            print("..............................................")
    time.sleep(1)
