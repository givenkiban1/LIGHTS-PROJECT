#command = 'python /home/pi/Documents/LIGHTS/buz.py'

import datetime
import time
import os
import sqlite3
import dbsys
import buz

database = "//home//pi//Documents//LIGHTS//db//sample.db"
conn = dbsys.create_connection(database)
cur = conn.cursor()


#Continue to loop through the program every second


while True:

    #Define day and time in loop so it alwats fetches current day and time.
    now= datetime.datetime.now()
    DayOfWeek = now.strftime("%A")
    CurrentTime = now.strftime("%H:%M:%S")

    #Get ring times for the current day.
    cur.execute("SELECT time(RingTime), RingDuration FROM Schedules WHERE EventDay = ? AND time(RingTime) = ?", [DayOfWeek, CurrentTime])
    #RingTimes=cur.fetchall()
    RingTimes = []
    RingDurations = []
    for row in cur.fetchall():
        RingTimes.append( row[0] )
        RingDurations.append( row[1] )
        
    RingDetails = []
    
    for row in cur.fetchall():
        RingDetails.append([row[0], row[1]])
        

    #Search through the array and ring bell when array times match current time to the second
    for o in RingDetails:
            if o[0]==str(CurrentTime):
                #os.system(command)
                buz.blink(o[1])
                print ("The current time is: ", CurrentTime)
                print ("Times Match. BELL RINGS @....", CurrentTime)
                print("..............................................")
        #           time.sleep(1)
    
        

