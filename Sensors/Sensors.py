#!/bin/python2

import GPIO
import time




class SR04:
    initialized=[]
    def initialize(TRIG,ECHO):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        self.initialized.append(TRIG)
    def takeDistance(self,TRIG,ECHO,trust=False,numIteration=1):
        if not TRIG in self.initialized:
            self.initialize(TRIG,ECHO)
        distance=[]
        for i in numIteration:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            StartTime = time.time()
            StopTime = time.time()
            while GPIO.input(ECHO) == 0:
                StartTime = time.time()
            while GPIO.input(ECHO) == 1:
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
    dist=SR04()
    dist.takeDistance(18,19)
