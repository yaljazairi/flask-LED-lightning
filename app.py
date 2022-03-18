from flask import Flask, render_template, request
import datetime
import getpass
import RPi.GPIO as GPIO

app = Flask(__name__)

# Name of logged-in User
username= getpass.getuser()
GPIO.setmode(GPIO.BCM)
# Red LED pin of choice
redLED_pin = 17
redLED_name= "redLED"
GPIO.setup(redLED_pin,GPIO.OUT)
redLED_status = GPIO.LOW
GPIO.output(redLED_pin,GPIO.LOW)

@app.route("/")
def home():
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%y %H:%M")
    # Status of red LED
    redLED_status= GPIO.input(redLED_pin)

    templateData = {
        'title': 'Flask Webserver',
        'user': username,
        'time': timeString,
        'redLED_pin': redLED_pin,
        'redLED_status': redLED_status
    }
    return render_template("index.html", **templateData)
    # return "Hallo {USERNAME}! <h1> in Flask :) </h1>"

@app.route("/<pinToChange>/<action>")
def action (pinToChange,action):
    pinToChange= int(redLED_pin)

    if action=="on":
        GPIO.output(pinToChange, GPIO.HIGH)
    
    if action=="off":
        GPIO.output(pinToChange, GPIO.LOW)

    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%y %H:%M")
    redLED_status= GPIO.input(redLED_pin)
    templateData ={
        'title': 'Flask Webserver',
        'user': username,
        'time': timeString,
        'redLED_pin': redLED_pin,
        'redLED_status': redLED_status
    }
    return render_template('index.html', **templateData)

if (__name__) == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
