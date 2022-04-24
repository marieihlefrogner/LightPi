import os, time, datetime, threading
import RPi.GPIO as GPIO
from pytz import timezone
from flask import *
from distance import *

queue = []

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

TRIG = 21
ECHO = 16

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    start = 0
    end = 0
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()
    
    while GPIO.input(ECHO) == True:
        end = time.time()

    return round((end-start) * 17150, 2)

def process_queue():
    while True:
        time.sleep(1)
        now = datetime.datetime.now() + datetime.timedelta(hours=2)
        
        for t in queue:
            if t[1] <= now:
                if t[0]:
                    os.system("~/wiringPi/on")
                else:
                    os.system("~/wiringPi/off")

                queue.remove(t)
            else:
                pass

        #print(get_distance(), "cm")


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", day=(datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y"), hour="10:30")

@app.route("/on")
def on():
    time.sleep(1)
    os.system("~/wiringPi/on")
    return redirect("/")

@app.route("/off")
def off():
    time.sleep(1)
    os.system("~/wiringPi/off")
    return redirect("/")

@app.route("/alarm", methods=['POST'])
def alarm():
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    date_in = request.form['date']
    time_in = request.form['time']
    on = 'alarm_on_off' in request.form

    print(now)
    
    try:
        datetime_in = datetime.datetime.strptime(date_in + " " + time_in, "%d/%m/%Y %H:%M")
    except:
        print("hack")
        return redirect("/")

    if now < datetime_in:
        if on:
            queue.append((True, datetime_in))
            print("Switching on at", datetime_in)
        else:
            queue.append((False, datetime_in))
            print("Switching off at", datetime_in)
        
    else:
        print("In the past:", datetime_in)

    return redirect("/")

if __name__ == "__main__":
    try:
        t = threading.Thread(target=process_queue)
        t.daemon = True
        t.start()
    except:
        print("Error: unable to start thread")
        exit()

    app.run(host="0.0.0.0", port=7001)
