import h5py
import numpy as np
import os
from scipy import ndimage
import matplotlib.image as mpimg
import sys
import json


for p,d,f in os.walk(sys.argv[1]):
    files = [(p + file, file) for file in f]

# populating X and y
X = np.zeros((len(files),1280,720,3))
y = []
for i, file in enumerate(files):
    print(file[1])
    X[i] = ndimage.imread(file[0])
    y.append(file[1])
    
asciiList = [n.encode("ascii") for n in y]

with h5py.File(os.path.join(sys.argv[1]+"images.h5"), "w") as file:
        file.create_dataset('images', 
                                       shape=X.shape, 
                                       compression=None,
                                       dtype='uint8',
                                       data=X)
        
        file.create_dataset('labels', (len(asciiList),1),'S30', asciiList)
        
