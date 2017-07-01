import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
import os.path

def loadSloth(imagesDir, annotationPos):
    # loading the annotations
    file = open(annotationPos, "r")
    loaded = json.load(file)
    d = {}
    for i in loaded:
        annotations = [a for a in i['annotations'] if a['class'] == 'rect']
        d[i["filename"]] = annotations

    # populating X and y
    X = []
    y = []
    for key,value in d.items():
        X.append(ndimage.imread(imagesDir+os.path.basename(key)))
        y.append(value)

    fileNames = d.keys()
    return X, y, fileNames

def saveSloth(fileNames, y):
    annotations = []
    for idx, imageName in enumerate(fileNames):
        entry = {
            "annotations" : y[idx],
            "class" : "rect",
            "filename" : imageName
        }
        annotations.append(entry)
    slothFile = json.dumps(annotations)
    return slothFile
