import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
import os.path
import sys

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

imagesDir = sys.argv[1]
jsonName = sys.argv[2]
csvPath = sys.argv[3]
xmin_img = 1
ymin_img = 1
xmax_img = 719
ymax_img = 1279

y,filenames = loadSloth(imagesDir,jsonName)

f = open(csvPath, "w+")
lines = []
for index, filepath in enumerate(filenames):
	filename = os.path.basename(filepath)
	image=ndimage.imread(os.path.join(imagesDir, filename))
	im_height, im_width, _ = image.shape
	for box in y[index]:
		#jsonName filepath, filename, xmin, ymin, xmax, ymax, class
		xmin = str(int(max(xmin_img, box['x'])))
		ymin = str(int(max(ymin_img, box['y'])))
		xmax = str(int(min(xmax_img, box['x']+box['width'])))
		ymax = str(int(min(ymax_img, box['y']+box['height'])))
		cl = "apple"
		f.write(', '.join((filename, xmin, ymin, xmax, ymax, cl,"\n")))
f.close()
