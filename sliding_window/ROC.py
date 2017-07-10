#%matplotlib inline
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from skimage import data
from scipy import misc
import h5py
from keras.utils.io_utils import HDF5Matrix
from quiver_engine import server

from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.models import Sequential, Model, model_from_json
from keras import backend as K
from keras.callbacks import TensorBoard
from keras import callbacks
from keras import optimizers
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator 
from keras.applications import VGG16
from keras.applications import ResNet50
from keras.layers import Input
from keras import utils as np_utils

from sys import exit

root_bad = './crop_bad/'
root_good = './crop_good/'

num_bad = 13571 #update
num_good = 9730
image_size = 224 #640

#X_train = HDF5Matrix('apples_classification_dataset.h5', 'X_train')
#Y_train = HDF5Matrix('apples_classification_dataset.h5', 'Y_train')
X_test = HDF5Matrix('apples_classification_dataset.h5', 'X_test')
Y_test = HDF5Matrix('apples_classification_dataset.h5', 'Y_test')

# build model
print("Building Model...")
resnet = VGG16(include_top=False, weights='imagenet', input_tensor=(Input(shape=(image_size, image_size, 3))))
for layer in resnet.layers:
    layer.trainable = False
print(resnet.summary())

x = Flatten(input_shape=resnet.output.shape)(resnet.output)

x = Dense(2048, activation='relu')(x)
x = Dropout(0.2)(x)

x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)

x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)

x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)

predictions = Dense(2, activation = 'softmax')(x)

model = Model(inputs=resnet.input, outputs=predictions)

#model = make_parallel(model, 2)

adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.load_weights("VGGConv_weights.h5")
loss, accuracy = model.evaluate(X_test, Y_test, verbose=0)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)


print("Generating ROC...")

#run test set, *1000 to prevent decimal issues
output = 1000*(model.predict(X_test))

num_pos = 0
num_neg = 0

print("Connecting labels and errors")
#connect label and error
roc = np.zeros((len(output),2))
print(output[0][0],Y_test[0][0])
for index,out in enumerate(output):
	roc[index,0] = out[0] #output of first node
	roc[index,1] = Y_test[index][0] #corresponding label
	if(Y_test[index][0]-1>-.1):
		num_pos+=1
	else:
		num_neg+=1

print("Sorting errors")
#sort by error (brief bubble sort)
for x in range(len(roc)-1):
	for y in range(x, len(roc)):
		if(roc[x,0]<roc[y,0]):
			temp = roc[x,0]
			temp2 = roc[x,1]
			roc[x,0] = roc[y,0]
			roc[x,1] = roc[y,1]
			roc[y,0] = temp
			roc[y,1] = temp2

print("Saving ROC")
f = open("ROC.txt","w")
#build curve
x0 = 0
y0 = 0
for i in range(len(roc)):
	#print(x0,y0)
	f.write(str(x0)+" "+str(y0)+"\n")
	if(roc[i][1]-1 > -.01):
		y0 = y0 + 1/num_pos
	else:
		x0 = x0 + 1/num_neg
f.close()

#use gnuplot
