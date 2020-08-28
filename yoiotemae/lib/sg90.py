from .sensor import Sensor

import requests
import RPi.GPIO as GPIO
import time

class Sg90(Sensor):

  def __init__(self, arg):
    self.argnum = 1

    self.gpio = int(arg[0])


  def rotate(self, pwm, fr, to):
    dire = 1
    if fr > to:
       dire = -1
    
    for degree in range(dire * fr, dire * to):
        dc = 2.5 + (12.0-2.5)/180*(dire * degree+90)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.03)
 

  def get(self):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.OUT)
    p = GPIO.PWM(self.gpio, 50)
    p.start(0.0)
    time.sleep(1.0)

    self.rotate(p, 90, -90)

    #for degree in range(-90, 90):
    #    dc = 2.5 + (12.0-2.5)/180*(-degree+90)
    #    p.ChangeDutyCycle(dc)
    #    time.sleep(0.03)

    time.sleep(2.0)

    self.rotate(p, -90, 90)
    #for degree in range(-90, 90):
    #    dc = 2.5 + (12.0-2.5)/180*(degree+90)
    #    p.ChangeDutyCycle(dc)
    #    time.sleep(0.03)

    p.ChangeDutyCycle(0.0)
    GPIO.cleanup()
    
    return [1]
