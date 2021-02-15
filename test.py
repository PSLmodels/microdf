import pandas as pd
import numpy as np
import microdf as mdf


arr = np.array([1, 2, 3])
w = np.array([4, 5, 6])
df = mdf.MicroDataFrame({"arr": arr}, weights=w)
df.arr
print(df.sum())
