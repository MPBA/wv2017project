#!/bin/python2

import cv2
import numpy
from PIL import Image
import time

class webCam():
    def __init__(self,port):
        self.cap=cv2.VideoCapture(port)

    def captureFrame(self):
        ret,frame=self.cap.read()
        return frame
    def computedFrame(self):
        return Image.fromarray(self.captureFrame(),'RGB')
    def showFrame(self):
        self.computedFrame().show()
    def saveFrame(self,path):
        seld.computedFrame().save(path)

def main():
    




if __name__=='__main__':
    main()
