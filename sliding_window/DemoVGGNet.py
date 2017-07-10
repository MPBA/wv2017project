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

image_size = 224 #640

# build model
print("Building Model...")
resnet = VGG16(include_top=False, weights='imagenet', input_tensor=(Input(shape=(image_size, image_size, 3))))
for layer in resnet.layers:
    layer.trainable = False
print(resnet.summary())

x = Flatten()(resnet.output)

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

adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.load_weights("VGG_weights_last.h5")
#yaml_string = (model.to_yaml())
#from keras.models import model_from_yaml
#model = model_from_yaml(yaml_string)
#print(model.summary())
#print(model.to_json())
server.launch(model, temp_folder="./quiver_temp", input_folder="./quiver_test", port=8090)
