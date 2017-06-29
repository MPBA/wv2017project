import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
from os import listdir
import sloth
import copy

def flipH(X,y):
    # not in place
    XX=copy.deepcopy(X)
    yy=copy.deepcopy(y)
    
    for idx in range(len(XX)):
        XX[idx] = np.fliplr(XX[idx])
        
    for idx, image in enumerate(yy):
        _,imWidth,_=XX[idx].shape
        for ann in image:
            ann['x']=imWidth-ann['x']-ann['width']
    return XX,yy


def flipV(X,y):
    # not in place
    XX=copy.deepcopy(X)
    yy=copy.deepcopy(y)
    
    for idx in range(len(XX)):
        XX[idx] = np.flipud(XX[idx])
        
    for idx, image in enumerate(yy):
        imHeight,_,_=XX[idx].shape
        for ann in image:
            ann['y']=imHeight-ann['y']-ann['height']
    return XX,yy

def rotate90(X,y):
    # not in place
    XX=copy.deepcopy(X)
    yy=copy.deepcopy(y)
    
    for idx, image in enumerate(yy):
        imHeight,imWidth,_=XX[idx].shape
        for ann in image:
            originalX=ann['x']
            originalW=ann['width']
            ann['x']=imHeight-ann['y']-ann['width']
            ann['y']=originalX
            ann['width']=ann['height']
            ann['height']=originalW
            
    for idx in range(len(XX)):
        XX[idx] = np.rot90(XX[idx],3)
        
    return XX,yy
    
def rotate270(X,y):
    # not in place
    XX=copy.deepcopy(X)
    yy=copy.deepcopy(y)
    
    for idx, image in enumerate(yy):
        imHeight,imWidth,_=XX[idx].shape
        for ann in image:
            originalX=ann['x']
            originalW=ann['width']
            ann['x']=ann['y']
            ann['y']=imWidth-originalX-ann['width']
            ann['width']=ann['height']
            ann['height']=originalW
            
    for idx in range(len(XX)):
        XX[idx] = np.rot90(XX[idx],1)
        
    return XX,yy

def rotate180(X,y):
    # not in place
    XX=copy.deepcopy(X)
    yy=copy.deepcopy(y)
    
    for idx, image in enumerate(yy):
        imHeight,imWidth,_=XX[idx].shape
        for ann in image:
            ann['x']=imWidth-ann['width']-ann['x']
            ann['y']=imHeight-ann['height']-ann['y']
            
    for idx in range(len(XX)):
        XX[idx] = np.rot90(XX[idx],2)
        
    return XX,yy

def augmentImage(X,y):
    newXs=[]
    newYs=[]
    newXs.extend(X)
    newYs.extend(y)
    a,b=flipH(X,y)
    newXs.extend(a)
    newYs.extend(b)
    a,b=flipV(X,y)
    newXs.extend(a)
    newYs.extend(b)
    a,b=rotate90(X,y)
    newXs.extend(a)
    newYs.extend(b)
    a,b=rotate180(X,y)
    newXs.extend(a)
    newYs.extend(b)
    a,b=rotate270(X,y)
    newXs.extend(a)
    newYs.extend(b)
    
    return newXs, newYs