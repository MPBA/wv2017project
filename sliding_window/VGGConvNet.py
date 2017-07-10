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

try:
        #X_train, X_test, Y_train, Y_test = map(np.load, ['X_train.npy',
        #                                                 'X_test.npy',
        #                                                 'y_train.npy',
        #                                                 'y_test.npy'])
        #with h5py.File("apple_classification.h5","r") as file:
        #file = h5py.File("apple_classification.h5","r")
        #X_train = file['X_train']
        #Y_train = file['Y_train']
        #X_test = file['X_test']
        #Y_test = file['Y_test']
        #print(X_train.shape,Y_train.shape,X_test.shape,Y_test.shape)
        #print(type(X_train),type(Y_train),type(X_test),type(Y_test))
        #file.close()
        X_train = HDF5Matrix('apples_classification_dataset.h5', 'X_train')
        X_train = X_train[0:15000]
        print(X_train.shape)
        Y_train = HDF5Matrix('apples_classification_dataset.h5', 'Y_train')
        Y_train = Y_train[0:15000]
        print(Y_train.shape)
        X_test = HDF5Matrix('apples_classification_dataset.h5', 'X_test')
        Y_test = HDF5Matrix('apples_classification_dataset.h5', 'Y_test')
except (IOError, KeyError):        
        print(e)
        
        '''
        X = np.zeros((num_bad+num_good,image_size,image_size,3))
        y = np.zeros((num_bad+num_good))

        print("Loading Bad Apples...")
        ctr = 0
        _,_,files = next(os.walk(root_bad))
        for file in files:
                if ctr<num_bad:
                        image = data.imread(os.path.join(root_bad,file))
                        image = image.astype(K.floatx())
                        X[ctr] = image[:,:,:3]/255.
                        y[ctr] = 1
                        ctr+=1	
        print("Loading Good Apples...")
        #print(ctr)
        _,_,files = next(os.walk(root_good))
        for file in files:
                if ctr<num_bad+num_good:
                        image = data.imread(os.path.join(root_good,file))
                        image = image.astype(K.floatx())
                        X[ctr] = image[:,:,:3]/255.
                        y[ctr] = 0
                        ctr+=1
                        
        print("Splitting Data...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Processing labels...")
        Y_train, Y_test = map(np_utils.to_categorical, [y_train, y_test])
        
        print("Saving data...")
        #np.save('X_train.npy', X_train)
        #np.save('X_test.npy', X_test)
        #np.save('Y_train.npy', Y_train)
        #np.save('Y_test.npy', Y_test)
        with h5py.File("apple_classification_float.h5","w") as file:
                file.create_dataset('X_train', shape=X_train.shape, compression=None, dtype='float32', data=X_train)
                file.create_dataset('Y_train', shape=Y_train.shape, compression=None, dtype='float32', data=Y_train)
                file.create_dataset('X_test', shape=X_test.shape, compression=None, dtype='float32', data=X_test)
                file.create_dataset('Y_test', shape=Y_test.shape, compression=None, dtype='float32', data=Y_test)
        exit()
        '''

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

load_weights = True
if(load_weights):
	model.load_weights("VGGConv_weights.h5")
	loss, accuracy = model.evaluate(X_test, Y_test, verbose=0)
	print('Test Loss:', loss)
	print('Test Accuracy:', accuracy)
        server.launch(model, temp_folder="./quiver_temp", input_folder="./quiver_test", port=8090)
else:
	print("Training Model...")
	early_stop = callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=4, verbose=0, mode='auto')
	checkpoint = callbacks.ModelCheckpoint("./checkpoint/weights.{epoch:02d}-{val_loss:.2f}.hdf5", save_weights_only=True,)
	callback = [early_stop, checkpoint]
        #model.fit_generator(datagen.flow(X_train, y_train, batch_size=16), steps_per_epoch=len(X_train) / 16, epochs=10, verbose=1, validation_data=(X_test, y_test), callbacks=early_stop)
	model.fit(X_train, Y_train, batch_size=48*2, epochs=100, verbose=1, validation_data=(X_test, Y_test), callbacks=callback, shuffle='batch')

	print("Saving Model...")
	model.save_weights("model_weights.h5")

'''
print("Generating ROC...")

#run test set
output = 1000*(model.predict(X_test))
#print(output.dtype)

num_pos = 0
num_neg = 0

print("Connecting labels and errors")
#connect label and error
roc = np.zeros((len(output),2))
for index,out in enumerate(output):
	roc[index,0] = out[0]
	roc[index,1] = Y_test[index][0]
	if(Y_test[index][0]-1>-.1):
		num_pos+=1
	else:
		num_neg+=1

print("Sorting errors")
#sort by error
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
'''
