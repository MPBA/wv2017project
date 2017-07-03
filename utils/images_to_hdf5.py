import h5py
import numpy as np
import os
from scipy import ndimage
import matplotlib.image as mpimg
import sys
import json

xmin_img = 1
ymin_img = 1
xmax_img = 719
ymax_img = 1279

def loadSloth(imagesDir, annotationPos):
    # loading the annotations
    file = open(annotationPos, "r")
    loaded = json.load(file)
    d = {}
    for i in loaded:
        annotations = [a for a in i['annotations'] if a['class'] == 'rect']
        if annotations:
            d[i["filename"]] = annotations

    # populating X and y
    X = []
    y = []
    for key,value in d.items():
        X.append(ndimage.imread(imagesDir+os.path.basename(key)))
        boxes=[]
        for box in value:
            xmin = max(xmin_img, box['x'])
            ymin = max(ymin_img, box['y'])
            xmax = min(xmax_img, box['x']+box['width'])
            ymax = min(ymax_img, box['y']+box['height'])
            boxes.append([xmin, ymin, xmax, ymax])
        y.append(boxes)
        
    file_names = d.keys()
    return X, y, file_names

# populating X and y
X , y, filenames = loadSloth(sys.argv[1], sys.argv[2]) 
X = np.array(X)
ascii_list = [n.encode("ascii") for n in filenames]

with h5py.File(os.path.join(sys.argv[1]+"images.h5"), "w") as file:
        file.create_dataset('images', 
                                       shape=X.shape, 
                                       compression=None,
                                       dtype='uint8',
                                       data=X)
        
        file.create_dataset('image_names', (len(ascii_list),1),'S30', ascii_list)
        dataset_boxes = file.create_group('/boxes')
        for i, entry in enumerate(y):
            dataset_boxes.create_dataset(str(i), data=entry)