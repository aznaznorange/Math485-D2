from lib.crxPandas import crx_data
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

df = pd.DataFrame(crx_data)
cols = df.columns.to_list()

x_cols = cols[0:-1]
y_cols = cols[-1:]

x = df.loc[:, x_cols]
y = df.loc[:, y_cols]

# x = StandardScaler().fit_transform(x)

pca = PCA(n_components=5)

x_pca = pca.fit_transform(x)