import h5py
import numpy as np
import os
from scipy import ndimage
import matplotlib.image as mpimg

with h5py.File("images.h5", "w") as file:
    for p,d,files in os.walk(sys.argv[1]):
        x_dset = file.create_dataset('images', 
                                       shape=[len(files), 
                                              1840, 3264, 3], 
                                       compression=None,
                                       dtype='uint8')
        for i, imagePath in enumerate([p+f for f in files]):
            image=mpimg.imread(imagePath).reshape(1840, 3264, 3)
            x_dset[i,]=image
