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

data = pd.read_csv("earthquake_datas.csv",
                        skiprows=1, delimiter=",",
                        names=["time", "magnitude", "longitude","Latitude","depth","rainfall"])

data_bc = data.copy()
data_bc.rainfall = data_bc.rainfall + 0.0001


for i in data_bc.columns:
    data_bc[i], _ = st.boxcox(data_bc[i])
std_scale_data = scale(data_bc)
std_data = pd.DataFrame(std_scale_data, columns = ["time", "magnitude", "longitude","Latitude","depth","rainfall"], index = data_bc.index)

model = KMeans(n_clusters=3, random_state=1)

model.fit(std_data)


silhouette_avg = silhouette_score(std_data, model.labels_)



fig = plt.figure()
ax = plt.axes(projection='3d')


ax.scatter(std_data.values[:,1],std_data.values[:,4],std_data.values[:,5],alpha=0.3,c=np.squeeze(model.labels_))

ax.set_xlabel('magnitude')
ax.set_ylabel('depth')
ax.set_zlabel('rainfall')
plt.savefig('result_safety_risk_assessment.png')