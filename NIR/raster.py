from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
import copy
#f = fopen('/home/wvstudent/2017_0628_092626_006.JPG', 'r');

picture = data.imread('test.JPG')
R = picture[:,:,0]
G = picture[:,:,1]
B = picture[:,:,2]

print("open")
plt.subplot(1,3,1)
print("step")
plt.imshow(B)
plt.subplot(1,3,2)
plt.imshow(R)
plt.subplot(1,3,3)
plt.imshow(G)
print("close")

image = (R-B)/(R+B)
print(image.shape)


level = image.min()
section = (image.max()-level)/10
refined = np.zeros((3024,4032,3))
refined[:][:][2] = 100
for i in range(0,10):
   for b in range(0,len(image[0])-1):
       for a in range(0,len(image)-1):
           if image[a][b] > level:
               refined[a,b,1] = 25*i
               refined[a,b,0] = 25*(10-i)
   level+= section

print(refined.shape)
plt.imshow(refined)
plt.show()
