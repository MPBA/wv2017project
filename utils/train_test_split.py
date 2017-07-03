import pandas as pd
import os
import numpy as np
import sys
import random as rnd

# argv[1] = filename
# argv[2] = train percentage


df = pd.read_csv(sys.argv[1], names=['filename','xmin','ymin','xmax','ymax','class'], index_col=False)
mask = [rnd.random()<float(sys.argv[2]) for _ in range(len(df))]
train = df[mask]
test = df[np.logical_not(mask)]

train.to_csv(sys.argv[1].replace('.csv','_train.csv') ,header=False, index=False)
test.to_csv(sys.argv[1].replace('.csv','_test.csv') ,header=False, index=False)
