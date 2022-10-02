from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn.preprocessing import scale
import csv
import scipy.stats as st
from sklearn.metrics import silhouette_score

import numpy as np
import pandas as pd

# time,magnitude,longitude,Latitude,depth,rainfall

# datas=np.loadtxt("earthquake_datas.csv",dtype=np.float,delimiter=',',skiprows=1)
data = pd.read_csv("earthquake_datas.csv",
                        skiprows=1, delimiter=",",
                        names=["time", "magnitude", "longitude","Latitude","depth","rainfall"])

# print(df.head())
data_bc = data.copy()
data_bc.rainfall = data_bc.rainfall + 0.0001

# boxcox转换
for i in data_bc.columns:  # 自动计算λ
    data_bc[i], _ = st.boxcox(data_bc[i])
std_scale_data = scale(data_bc) # 标准化
std_data = pd.DataFrame(std_scale_data, columns = ["time", "magnitude", "longitude","Latitude","depth","rainfall"], index = data_bc.index)

model = KMeans(n_clusters=3, random_state=1)

model.fit(std_data)

print(std_data.head())

silhouette_avg = silhouette_score(std_data, model.labels_)
print(silhouette_avg)

#定義座標軸
fig = plt.figure()
ax = plt.axes(projection='3d')

#作圖
ax.scatter(std_data.values[:,1],std_data.values[:,4],std_data.values[:,5],alpha=0.3,c=np.squeeze(model.labels_))

print(model.labels_)


# print(datas[:,1])
# print(datas[:,4])
# print(datas[:,5])
# plt.xlabel('magnitude')
# plt.ylabel('depth')
# plt.clabel('rainfall')

ax.set_xlabel('magnitude')
ax.set_ylabel('depth')
ax.set_zlabel('rainfall')
plt.show()


# scatter = plt.scatter(datas[:,1], datas[:,4], c=np.squeeze(model.labels_))
