import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
GPIO.output(2,GPIO.LOW)



def blink():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(2,GPIO.OUT)
    print('LED ON')
    GPIO.output(2,GPIO.HIGH)
    time.sleep(1)
    print('LED OFF')
    GPIO.output(2,GPIO.LOW)
