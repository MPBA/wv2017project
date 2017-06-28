import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
from os import listdir

def loadSloth(imagesDir, annotationPos):
    # loading the annotations
    fileNames = listdir(imagesDir)
    file = open(annotationPos, "r")
    loaded=json.load(file)
    d={}
    for i in loaded:
        d[i["filename"]]=i["annotations"]
    
    # populating X and y
    X=[]
    y=[]
    for imageName in fileNames:
        X.append(ndimage.imread(imagesDir+imageName))
        y.append(d[imageName])
    return X,y,fileNames

def saveSloth(fileNames, y):
    annotations=[]
    for idx, imageName in enumerate(fileNames):
        entry={
            "annotations": y[idx],
            "class": "image",
            "filename": imageName
        }
        annotations.append(entry)
    slothFile=json.dumps(annotations)
    return slothFile
