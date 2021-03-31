from picamera import PiCamera
import time
from time import sleep
import os
import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import Button
import serial
import requests


switch = Button(26)
buzzer = LED(16)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance




buzzer.off()

while True:
    switch_state=GPIO.input(26)
    print(switch_state)

    if switch_state==0:
        r =requests.get('http://www.iotclouddata.com/20log/336/iot20.php?A=A')
        buzzer.on()
        sleep(2)
        buzzer.off()

    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
    time.sleep(1)
    

    if dist<10:
        r =requests.get('http://www.iotclouddata.com/20log/336/iot20.php?A=A')
        buzzer.on()
        sleep(2)
        buzzer.off()
