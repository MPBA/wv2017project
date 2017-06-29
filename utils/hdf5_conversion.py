import h5py
import numpy as np
import slothutils

imgs = './JPG_Images/'
annotations = './Annotated_Images/one.json'

def jpg_to_h5(imgs, annotations):
    X, y, fileNames = slothutils.loadSloth(imgs, annotations)
    
    #create new h5 file
    f = h5py.File("images.hdf5", "w")

    #create 2 datasets within h5 file
    x_dset = f.create_dataset("x_dataset", (len(X),0), dtype='i')
    y_dset = f.create_dataset("y_dataset", (len(y),0), dtype='i')
    
    for i in range(len(X)):
        x_dset[i,] = X[i]
        y_dset[i,] = y[i]
    
    return f, x_dset, y_dset