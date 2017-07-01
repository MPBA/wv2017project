import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
import os.path

def loadSloth(imagesDir, annotationPos):
	# loading the annotations
	file = open(annotationPos, "r")
	loaded=json.load(file)
	d={}
	for i in loaded:
		annotations=[a for a in i['annotations'] if a['class']=='rect']
		d[i["filename"]]= annotations
    
	# populating X and y
	#X=[]
	y=[]
	for key,value in d.items():
		#X.append(ndimage.imread(imagesDir+os.path.basename(key)))
		y.append(value)

	fileNames=d.keys()
	#return X,y,fileNames
	return y, fileNames

y,filenames = loadSloth("./conv/","04_Andrea_Zanin.json")
print(len(y),len(filenames))

f = open("annotations.csv", "w")
lines = []
for index, filename in enumerate(filenames):
	filename = filename.split("/")[-1]
	for box in y[index]:
		f.write(filename+", "+str(box['x'])+", "+str(box['x']+box['width'])+", "+str(box['y'])+", "+str(box['y']+box['height'])+"\n")
f.close()
