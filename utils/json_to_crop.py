import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib import patches
import json
import os.path
from skimage import data

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

outputDir = sys.argv[1]+"crop/"
imagesDir = sys.argv[1]+"conv/"
jsonName = sys.argv[2]
xmin_img = 1
ymin_img = 1
xmax_img = 719
ymax_img = 1279

#X, y, filenames = loadSloth(imagesDir,jsonName)
y, filenames = loadSloth(imagesDir,jsonName)


lines = []
for index, filepath in enumerate(filenames):
	filename = filepath.split("/")[-1]
	image = data.imread(os.path.join(imagesDir,filename))
	for index, box in enumerate(y[index]):
		width = box['width']
		height = box['height']
		if( abs((width-height)/(width+height))<.17):
			xmin = str(max(xmin_img, box['x']))
			ymin = str(max(ymin_img, box['y']))
			xmax = str(min(xmax_img, box['x']+width))
			ymax = str(min(ymax_img, box['y']+height))
			crop_image = image[xmin:xmax,ymin:ymax]
			plt.imsave(outputDir+str(index)+'.png',crop_image)  

