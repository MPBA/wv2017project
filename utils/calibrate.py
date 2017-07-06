#%matplotlib inline
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from scipy import misc

root_input = './Labeled/'
root_output = './Scaled_Labels/'
#_,_,files = next(os.walk(root_input))
#num_files = len(files)

#Smallest image is 638 x 638 but we do 640 x 640
for prefix,_,files in os.walk(root_input):
	if("GOOD" in prefix):
		root_output = "./Scaled_Labels/Label_Good/"
	else:
		root_output = "./Scaled_Labels/Label_Bad/"
	num_files = len(files)
	for index, file in enumerate(files):
		if(index%10==0):
			print(str(index)+"/"+str(num_files))
		image = data.imread(os.path.join(prefix,file))
		min_dim = min(len(image),len(image[0]))
		crop_image = image[0:min_dim,0:min_dim]
		scale_image = misc.imresize(crop_image,(224,224,3))
		plt.imsave(root_output+str(index)+'.png',scale_image)  

'''
images=[]
for file in files:
    images.append(data.imread(os.path.join(root_input,file)))

for index, image in enumerate(images):
	plt.imsave(root_output+str(index)+'.png',image)  
'''

