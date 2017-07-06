import pandas as pd
import sys
import os

imageDir=sys.argv[1]
filepath=sys.argv[2]
df = pd.read_csv(filepath, names=['filename','xmin','xmax','ymin','ymax','class'], index_col=False)
df['filename']=[os.path.join(imageDir,a) for a in df['filename']]

df.to_csv('fout.csv', mode='a', index=False, header=False)
