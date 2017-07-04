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

from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.models import Sequential, Model
from keras import backend as K
from keras.callbacks import TensorBoard
from keras import optimizers
from keras.models import load_model
from keras.applications import VGG16
from keras.layers import Input
from keras import utils as np_utils
from keras.preprocessing import image

root = './test_images/'
root_out = '/test_out/'

image_size = 224
filter_size = 50

# rebuild model
print("Building Model...")
vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=(Input(shape=(image_size, image_size, 3))))
for layer in vgg16.layers:
	layer.trainable = False

x = Flatten(input_shape=vgg16.output.shape)(vgg16.output)
x = Dense(2048, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
predictions = Dense(2, activation = 'softmax')(x)

model = Model(inputs=vgg16.input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.load_weights("model_weights.h5")

#Run on images
_,_,files = next(os.walk(root))
count = np.zeros(len(files))
for index, img_name in enumerate(files):
	#img = data.imread(os.path.join(root,img_name))
	img_raw = image.load_img(os.path.join(root,img_name)) #load with keras
	img = image.img_to_array(img_raw)[0:3] #convert to array and cut last axis
	width = len(img)
	height = len(img[0])
	num_total = 0
	num_apple = 0
	for w in range(0, width-filter_zize, filter_size/2):
		for h in range(0, height-filter_size, filter_size/2):
			num_total+=1
			test_img = img[w:w+filter_size,h:h+filter_size,:]
			proc_img = preprocess_input(test_img) #preproc
			#y = model.predict(proc_img)
			#if(y[0]>.5):
			#	num_apple+=1
	if(num_apple > num_total-num_apple):
		num_apple = num_total-num_apple
		print("Stuff went down!!")
	count[index] = num_apple
for i in count:
	print(i)

