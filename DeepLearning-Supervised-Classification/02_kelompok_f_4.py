# -*- coding: utf-8 -*-
"""02-Kelompok F-4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bIbA9Wiy5069j3bSRx78wWsO9BAMd2vw

# Assignment Chapter 2 - DEEP LEARNING [Case #4]
Startup Campus, Indonesia - `Artificial Intelligence (AI)` (Batch 7)
* Task: **CLASSIFICATION**
* DL Framework: **PyTorch**
* Dataset: Credit Card Fraud 2023
* Libraries: Pandas/cuDF, Scikit-learn/cuML, Numpy/cuPy
* Objective: Classify credit fraud transactions using Multilayer Perceptron

`PERSYARATAN` Semua modul (termasuk versi yang sesuai) sudah di-install dengan benar.
<br>`CARA PENGERJAAN` Lengkapi baris kode yang ditandai dengan **#TODO**.
<br>`TARGET PORTFOLIO` Peserta mampu mengklasifikasi transaksi fraud menggunakan *Multilayer Perceptron*

### Import Libraries
"""

!git clone https://github.com/rapidsai/rapidsai-csp-utils.git
!python rapidsai-csp-utils/colab/pip-install.py

import shutil
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

"""<font color="red">**- - - - MOHON DIPERHATIKAN - - - -**</font>
<br>**Aktifkan GPU sekarang.** Di Google Colab, klik **Runtime > Change Runtime Type**, lalu pilih **T4 GPU**.

### Dataset Loading (CPU vs. GPU)
"""

from pandas import read_csv as read_by_CPU
from cudf import read_csv as read_by_GPU

# unzip the file
shutil.unpack_archive('dataset_case_04.zip', '/content/sample_data/', 'zip')

# Commented out IPython magic to ensure Python compatibility.
# TODO: Impor dataset dengan Pandas, gunakan fungsi "read_by_CPU"
# %time data_cpu = read_by_CPU('/content/sample_data/creditcard_2023.csv')

# Commented out IPython magic to ensure Python compatibility.
# Impor dataset dengan cuDF (Pandas di GPU)
# %time data_gpu = read_by_GPU('/content/sample_data/creditcard_2023.csv')

# TODO: Hilangkan kolom ID
data_gpu = data_gpu.drop(columns=["id"])

"""### Standardization (CPU vs. GPU)"""

from sklearn.preprocessing import StandardScaler as StandardScalerCPU
from cuml.preprocessing import StandardScaler as StandardScalerGPU

ScalerCPU = StandardScalerCPU()
ScalerGPU = StandardScalerGPU()

arbitrary_features = ["V"+str(i+1) for i in range(27)]

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# data_cpu[arbitrary_features] = ScalerCPU.fit_transform(data_cpu[arbitrary_features].values)
# data_cpu["Amount"] = ScalerCPU.fit_transform(data_cpu["Amount"].values.reshape(-1, 1)).squeeze()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# data_gpu[arbitrary_features] = ScalerGPU.fit_transform(data_gpu[arbitrary_features].values)
# data_gpu["Amount"] = ScalerGPU.fit_transform(data_gpu["Amount"].values.reshape(-1, 1)).squeeze()

"""### Train/Test Split (CPU vs. GPU)"""

from sklearn.model_selection import train_test_split as splitCPU
from cuml.preprocessing import train_test_split as splitGPU

# TODO: Tentukan X (features) dan Y (target), gunakan "data_gpu"
X = data_gpu.drop(columns=["Class"])
Y = data_gpu["Class"]

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # TODO: Pecah dataset dengan komposisi 80% train set dan 20% test set, dengan fungsi "splitCPU"
# test_size = .2
# random_state = 42
# x_train, x_test, y_train, y_test = splitCPU(X, Y, test_size=test_size, random_state=random_state)
# 
# print("x_train shape: ", x_train.shape)
# print("x_test shape: ", x_test.shape)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # TODO: Lakukan hal yang sama untuk data spliting, tetapi dengan fungsi "splitGPU"
# test_size = .2
# random_state = 42
# x_train, x_test, y_train, y_test = splitGPU(X, Y, test_size=test_size, random_state=random_state)
# 
# print("x_train shape: ", x_train.shape)
# print("x_test shape: ", x_test.shape)

"""### Convert the dataset into Tensor"""

import cupy # Numpy for GPU

# TODO: Aktifkan GPU (CUDA) sebagai device untuk training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())

# code tambahan untuk mengkonvert hasil data spliting
x_train = x_train.to_cupy()
y_train = y_train.to_cupy()
x_test = x_test.to_cupy()
y_test = y_test.to_cupy()

x_train_tensor = torch.from_numpy(cupy.asnumpy(x_train)).to(device)
y_train_tensor = torch.from_numpy(cupy.asnumpy(y_train)).to(device)

x_test_tensor = torch.from_numpy(cupy.asnumpy(x_test)).to(device)
y_test_tensor = torch.from_numpy(cupy.asnumpy(y_test)).to(device)

Train_tensor = TensorDataset(x_train_tensor, y_train_tensor)
Test_tensor = TensorDataset(x_test_tensor, y_test_tensor)

"""### Batching the Dataset with PyTorch DataLoader"""

# TODO: Tentukan nilai batch
batch_size = 64

Train_dataset = DataLoader(Train_tensor, batch_size=batch_size, shuffle=True)
Test_dataset = DataLoader(Test_tensor, batch_size=batch_size, shuffle=False)

"""### Model Blueprint"""

class FeedForward(nn.Module):
    def __init__(self, input_dim, num_neurons):
        super(FeedForward, self).__init__()
        self.input_dim = input_dim
        self.num_neurons = num_neurons

        self.net = nn.Sequential(
            nn.Linear(self.input_dim, self.num_neurons),
            nn.ReLU()
        )

    def forward(self, x):
        return self.net(x)

    def to(self, device):
        self.net.to(device)
        return self

class Net(nn.Module):
    def __init__(self, in_features, num_layers, num_neurons):
        super(Net, self).__init__()
        self.in_features = in_features
        self.num_layers = num_layers
        self.num_neurons = num_neurons

        self.fc1 = nn.Linear(self.in_features, self.num_neurons)
        self.relu = nn.ReLU()
        self.blocks = [FeedForward(self.num_neurons, self.num_neurons).to(device) \
                       for _ in range(self.num_layers)]
        self.output_layer = nn.Linear(self.num_neurons, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        output = self.relu(self.fc1(x))

        for block in self.blocks:
            output = block(output)
        output = self.sigmoid(self.output_layer(output))

        return output

"""### Model Hyperparameters and Parameters"""

# [ PERTANYAAN ]
# Apa perbedaan hyperparameters dan parameters?

"""[ ANSWER HERE ]

**Hyperparameter**
*   Didefinisikan diawal pembuatan model
*   Tidak menempel pada model tapi hyperparameter adalah sesuatu yang didefinisikan untuk mengoptimalisasi model

**Parameter**
*   Dihasilkan diakhir oleh model setelah model di training
*   Parameter adalah sesuatu yang berada dalam model


Intiya parameter adalah nilai model yang di pelajari otomatis dari data, sedangkan hyperparameter itu kita tentukan sendiri untuk membangun model
"""

# TODO: Tentukan hyperparameters
epochs = 30
num_layers = 3
num_neurons = 128
learning_rate = 0.001

# TODO: Tentukan besaran input untuk model
num_inputs = 29

model = Net(in_features=num_inputs, num_layers=num_layers, num_neurons=num_neurons)
model = model.to(device)

# Set the optimizer and loss function
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
criterion = nn.BCELoss()

# Check the number of parameters
print("Number of parameters: {:,}".format(sum(p.numel() for p in model.parameters() if p.requires_grad)))
print("Number of trainable parameters: {:,}".format(sum(p.numel() for p in model.parameters() if p.requires_grad)))

# [ PERTANYAAN ]
# Mengapa total "trainable parameters" sama dengan total keseluruhan parameter?

"""[ ANSWER HERE ]

Total "trainable parameters" sama dengan total keseluruhan parameter karena semua parameter yang ada dalam model tersebut diatur (dapat diperbarui) untuk dapat dilatih (trainable). Ini berarti tidak ada parameter yang dibekukan (frozen) atau ditetapkan sebagai tidak dapat dilatih, parameter yang dapat dilatih (trainable parameters) adalah bobot dan bias yang diperbarui oleh optimizer untuk meminimalkan loss.

Jika parameter tertentu tidak ditandai sebagai non-trainable (misalnya seperti model diatas, dengan requires_grad=False), maka semua parameter dalam model tersebut akan tetap trainable. Artinya, semua parameter dalam model yang diatur untuk dapat dilatih menghasilkan total "trainable parameters" yang sama dengan total keseluruhan parameter.

### Train the Model
"""

print("Start training ...")
for epoch in range(epochs):
    train_loss = 0.0
    model.train()

    for data, label in Train_dataset:
        data = data.to(device)
        label = label.squeeze()
        label = label.to(device)
        optimizer.zero_grad()
        output = model.forward(data.float())

        loss = criterion(output.squeeze(), label.float())
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    train_loss = train_loss / len(Train_dataset.dataset)
    if(epoch % 10 == 0):
        print('  - Epoch: {} \tTraining_loss: {:.6f}'.format(epoch, train_loss))

"""### Model ACCURACY should reach >= 95%"""

# TODO: Jika akurasi masih dibawah 95%, silakan lakukan fine-tuning

correct_preds = 0
total_samples = 0

with torch.no_grad():
    for data, labels in Test_dataset:
        labels = labels.squeeze()
        output = model.forward(data.float())
        output = output.squeeze(1)

        predictions = (output >= 0.5).float()
        correct_preds += (predictions == labels).sum().item()
        total_samples += labels.numel()

accuracy = correct_preds / total_samples
print("Model accuracy: {:.2f}%".format(accuracy*100))

"""### Scoring
Total `#TODO` = 12
<br>Checklist:

- [✔️] Impor dataset dengan Pandas, gunakan fungsi "read_by_CPU"
- [✔️] Hilangkan kolom ID
- [✔️] Tentukan X (features) dan Y (target), gunakan "data_gpu"
- [✔️] Pecah dataset dengan komposisi 80% train set dan 20% test set, dengan fungsi "splitCPU"
- [✔️] Lakukan hal yang sama untuk data spliting, tetapi dengan fungsi "splitGPU"
- [✔️] Aktifkan GPU (CUDA) sebagai device untuk training
- [✔️] Tentukan nilai batch
- [✔️] PERTANYAAN: Apa perbedaan hyperparameters dan parameters?
- [✔️] Tentukan hyperparameters
- [✔️] Tentukan besaran input untuk model
- [✔️] PERTANYAAN: Mengapa total "trainable parameters" sama dengan total keseluruhan parameter?
- [✔️] Jika akurasi masih dibawah 95%, silakan lakukan fine-tuning

### Additional readings
- N/A

### Copyright © 2024 Startup Campus, Indonesia
* Prepared by **Nicholas Dominic, M.Kom.** [(profile)](https://linkedin.com/in/nicholas-dominic)
* You may **NOT** use this file except there is written permission from PT. Kampus Merdeka Belajar (Startup Campus).
* Please address your questions to mentors.
"""