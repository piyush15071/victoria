# import RPi.GPIO as GPIO
from time import sleep

def on():
    # no console output for GPIO cleanup
    GPIO.setwarnings(False)
    
    # refer to the GPIO pins on RPi
    GPIO.setmode(GPIO.BCM)

    # set 18 as output
    GPIO.setup(18, GPIO.OUT)
    
    # Turn off the led, as it might already be on
    GPIO.output(18, GPIO.LOW)

    sleep(0.1)
    # On
    GPIO.output(18, GPIO.HIGH)

def off():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    
    # Off
    GPIO.output(18, GPIO.LOW)

    # clean all the channels after using
    GPIO.cleanup(18)