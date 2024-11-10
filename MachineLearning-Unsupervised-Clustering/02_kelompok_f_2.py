# -*- coding: utf-8 -*-
"""02-Kelompok F-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1om2sk_wu-QzUON8_LA7fQW0pIYzl1rUc

# Assignment Chapter 2 - MACHINE LEARNING [Case #2]
Startup Campus, Indonesia - `Artificial Intelligence (AI)` (Batch 7)
* Dataset: cluster_s1
* Libraries: Pandas, Numpy, Scikit-learn, Matplotlib, Seaborn
* Objective: Data Segmentation with KMeans Clustering

`PERSYARATAN` Semua modul (termasuk versi yang sesuai) sudah di-install dengan benar.
<br>`CARA PENGERJAAN` Lengkapi baris kode yang ditandai dengan **#TODO**.
<br>`TARGET PORTFOLIO` Peserta mampu membandingkan akurasi klasifikasi dari berbagai model *supervised learning*.

### Import Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import cluster
from sklearn.metrics import silhouette_score

"""### Read Dataset"""

data = pd.read_csv('https://raw.githubusercontent.com/Rietaros/kampus_merdeka/main/cluster_s1.csv')
data = data.drop('no', axis = 1)
data.head()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
ax1 = data.plot.scatter(x='x', y='y', c='DarkBlue')

"""### Data Segmentation (Clustering)"""

# TODO: Lakukan pencarian jumlah cluster terbaik berdasarkan data diatas
# Menentukan jumlah cluster terbaik dengan metode Elbow method
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

values = [KMeans(n_clusters=k, random_state=12).fit(data).inertia_ for k in range(2, 29)]

# Menyimpan hasil ke dalam DataFrame
el = pd.DataFrame({"Inertia": values}, index=range(2, 29))

# Plot show
el.plot(kind='line')
plt.ylabel("Value")
plt.xlabel("Number of cluster")
plt.title("Elbow Method for KMeans")
plt.show()

# TODO: Lakukan pemodelan dengan KMeans
kmeans = cluster.KMeans(n_clusters=15, random_state=42)
kmeans.fit(data)
labels = kmeans.labels_

score = silhouette_score(data, labels)
print("silhouette score={:.5f}".format(score))

"""### Visualization: Cluster Result"""

# TODO: Masukkan label hasil clustering ke dalam DataFrame

result = data.copy()
result['cluster'] = labels
print(result.head())

# TODO: Plot data hasil clustering dengan Seaborn
plt.figure(figsize=(12, 8))
sns.scatterplot(data=result, x='x', y='y', hue='cluster', palette='viridis', style='cluster', markers=['o', 's', 'D', 'X'], s=100)
plt.title('Data Hasil Clustering dengan KMeans')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(title='Cluster')
plt.grid()
plt.show()

"""### Scoring
Total `#TODO` = 4
<br>Checklist:

- [✔️] Lakukan pencarian jumlah cluster terbaik berdasarkan data diatas
- [✔️] Lakukan pemodelan dengan KMeans
- [✔️] Masukkan label hasil clustering ke dalam DataFrame
- [✔️] Plot data hasil clustering dengan Seaborn

### Additional readings
- N/A

### Copyright © 2024 Startup Campus, Indonesia
* You may **NOT** use this file except there is written permission from PT. Kampus Merdeka Belajar (Startup Campus).
* Please address your questions to mentors.
"""