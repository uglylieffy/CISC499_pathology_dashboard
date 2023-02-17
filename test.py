import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cm as cm
import seaborn
df = pd.DataFrame({
    'length': [1.5, 0.5, 1.2, 0.9, 3],
    'width': [0.7, 0.2, 0.15, 0.2, 1.1]
    }, index=['pig', 'rabbit', 'duck', 'chicken', 'horse'])
hist = df.hist(bins=3)
plt.show()