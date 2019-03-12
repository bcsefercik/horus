import json

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np


dataRaw = None
macDict = None

with open("20181218-1730_ArcelikInnovationOffice.json") as f:
	dataRaw = json.load(f)

with open("20181218-1730_ArcelikInnovationOffice_macdict.json") as f:
	macDict = json.load(f)

data = np.zeros([len(dataRaw), len(macDict)], dtype = float) - 100
labels = np.zeros([len(dataRaw)], dtype = int)

locationDict = {}

for i in range(len(dataRaw)):
	if isinstance(locationDict.get(dataRaw[i]["tag"], None), type(None)):
		locationDict[dataRaw[i]["tag"]] = len(locationDict)

	labels[i] = locationDict[dataRaw[i]["tag"]]

	for ap in dataRaw[i]["result"]:
		data[i][macDict[ap["macAddress"]] - 1] = ap["rssi"]

# data = np.abs(data)
dataNormalized = (data - np.mean(data, 0)) / (np.std(data, 0) + 1e-100)

model = keras.Sequential([
    keras.layers.Dense(len(locationDict), activation=tf.nn.softmax)
])

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(dataNormalized, labels, epochs=5)


model.predict((np.expand_dims(data[3],0)))