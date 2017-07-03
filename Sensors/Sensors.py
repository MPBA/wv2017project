#!/bin/python2

import GPIO
import time

Trigger=18
Echo=24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def takeDistance(trust=False,numIteration=1):
    distance=[]
    for i in numIteration:
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance.append((TimeElapsed * 34300) / 2)
    medDistance=0
    for i in distance:
        medDistance+=i
    medDistance/=len(distance)
    if trust:
        for i in distance:
            if abs(medDistance-i)/medDistance > 0.1:
                return False
    return medDistance



if __name__='__main__':
    distance=takeDistance(2)
