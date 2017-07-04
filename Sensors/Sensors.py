import RPi.GPIO as GPIO
import time
#import rospy
#from mavros_msgs.msg import ManualControl

'''
class publish:
    def __init__:
        self.pub=rospy.Publisher("manual_control/control",ManualControl, queue_size=1)
        rospy.init_node('SR04', anonymous=False)
        rate = rospy.Rate(10) # 10hz
    def pub(values)
        self.pub.publish(values)
'''

class SR04:
    initialized=[]
    def initialize(self,TRIG,ECHO):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        self.initialized.append(TRIG)
    def takeDistance(self,TRIG=None,ECHO=None,couple=None,trust=False,numIteration=1):
        #if couple:
            #TRIG=couple[0]
            #ECHO=couple[1]
        if not TRIG in self.initialized:
            self.initialize(TRIG,ECHO)
        distance=[]
        for i in range(numIteration):
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



if __name__=='__main__':
    GPIO.setmode(GPIO.BOARD)
    dist=SR04()
    while True:
        print dist.takeDistance(TRIG=11,ECHO=13)
        time.sleep(0.1)
