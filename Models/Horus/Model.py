# -*- coding: utf-8 -*-
import json

import numpy as np

import inlo_utils as iu
import data_tool as dt

from ..ModelInterface import ModelInterface

class Horus():
	def __init__(self, paramsPath, datasetPath=None):
		self.params = paramsPath
		self.data = None
		if datasetPath:
			self.loadDataset(datasetPath)


	def loadDataset(self, datasetPath):
		with open(datasetPath, encoding='utf-8') as json_file:
			self.data = json.load(json_file)

	def radioMapBuilder(self):
		status = 0
		if isinstance(self.data, type(None)):
			status = 1
			return status, None

		return dt.createLocationRSSISeries(self.data)

	def sortedAP(self, location, n=0):
		unsortedDict = {k: location[k]["mean"] if location[k].get("mean") else (np.mean(location[k]["rssiSeries"]) if location[k].get("rssiSeries") else location[k]) for k in location}
		sortedLocations = list(map(lambda x: x[0], sorted(unsortedDict.items(), key=lambda kv: kv[1], reverse=True)))
		return sortedLocations[0:min(n, len(sortedLocations))] if n > 0 else sortedLocations

	# def sortedAPRadioMap(self, radioMap):
	# 	status = 0
		
	# 	if not (isinstance(radioMap, dict) and len(radioMap)>0):
	# 		status = 1
	# 		return status, None

	# 	{l: for l in radioMap}





class Model(ModelInterface):
	"""docstring for Model"""
	def __init__(self, paramsPath, debugMode=False):
		ModelInterface.__init__(self, paramsPath, debugMode=debugMode)
		self.horus = Horus(paramsPath)
		
	def train(self, datasetPath):
		self.horus.loadDataset(datasetPath)
		self.horus.radioMapBuilder()

	def predict(self, rssi):
		return 0,2
