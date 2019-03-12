# -*- coding: utf-8 -*-
import json
import pickle

import numpy as np

import inlo_utils as iu
import data_tool as dt

from ..ModelInterface import ModelInterface

class Horus():
	def __init__(self, datasetPath=None):
		self.data = None

		if datasetPath:
			self.loadDataset(datasetPath)
		
		self.macDict = None
		self.k = 10
		self.q = 2
		self.radioMap = None
		self.clusters = {"keys": None, "locations": None}

	def saveParameters(self, paramsPath):
		params = {	"macDict": self.macDict, 
					"k": self.k, 
					"q": self.q, 
					"radioMap": self.radioMap, 
					"clusterKeys": self.clusters["keys"],
					"clusterLocations": self.clusters["locations"]
				}

		with open(paramsPath, 'wb') as f:
			pickle.dump(params, f, pickle.HIGHEST_PROTOCOL)

	def loadParameters(self, paramsPath):
		params = None
		with open(paramsPath, 'rb') as f:
			params = pickle.load(f)

		self.macDict = params["macDict"]
		self.k = params["k"]
		self.q = params["q"]
		self.radioMap = params["radioMap"]
		self.clusters["keys"] = params["clusterKeys"]
		self.clusters["locations"] = params["clusterLocations"]
		# print(params)

	def loadDataset(self, datasetPath):
		with open(datasetPath, encoding='utf-8') as json_file:
			self.data = json.load(json_file)
		self.macDict = dt.createMacDict(self.data)

	def radioMapBuilder(self):
		status = 0
		if isinstance(self.data, type(None)):
			status = 1
			return status, None

		methodStatus, self.radioMap = dt.createLocationRSSISeries(self.data, macDict = self.macDict)

		if methodStatus != 0:
			status = 2
			self.radioMap = None
			return status

		return status

	def sortedAP(self, rssiDict, n=0):
		sortedLocations = list(map(lambda x: x[0], sorted(rssiDict.items(), key=lambda kv: kv[1], reverse=True)))
		return sortedLocations[0:min(n, len(sortedLocations))] if n > 0 else sortedLocations 

	def sortedAPOffline(self, location, n=0):
		unsortedDict = {k: location[k]["mean"] if location[k].get("mean") else (np.mean(location[k]["rssiSeries"]) if location[k].get("rssiSeries") else location[k]) for k in location}
		sortedLocations = list(map(lambda x: x[0], sorted(unsortedDict.items(), key=lambda kv: kv[1], reverse=True)))
		return sortedLocations[0:min(n, len(sortedLocations))] if n > 0 else sortedLocations

	def sortedAPRadioMap(self, n=0):
		status = 0
		
		if not (isinstance(self.radioMap, dict) and len(self.radioMap)>0):
			status = 1
			return status, None

		for locationTag in self.radioMap:
			self.radioMap[locationTag]["sortedAP"] = self.sortedAPOffline(self.radioMap[locationTag], n=n)

		return status

	def createClusters(self, k=0, q=0):
		status = 0
		if k == 0:
			k = self.k
		if q == 0:
			q = self.q

		selectedAPs = {l: self.radioMap[l]["sortedAP"][0:k] for l in self.radioMap}
		clusterKeys = []
		clusterElements = []

		for locationTag in selectedAPs:
			clusterKey = set(selectedAPs[locationTag][0:q])
			
			if not clusterKey in clusterKeys:
				clusterKeys.append(clusterKey)
				clusterElements.append([])

			clusterElements[clusterKeys.index(clusterKey)].append(locationTag)

		self.clusters["keys"] = clusterKeys
		self.clusters["locations"] = clusterElements

		return status

	def findCluster(self, sortedAP, clusterKeys = None, clusterElements = None, q = 0):
		status = 0
		clusterIndices = []
		locationCandidates = []

		if iu.isNone(clusterKeys) or iu.isNone(clusterElements):
			clusterKeys = self.clusters["keys"]
			clusterElements = self.clusters["locations"]

		if q == 0:
			q = min(self.q, len(sortedAP))
		
		if q == 0:
			status = 1
			return status, clusterIndices, locationCandidates

		searchKey = set(sortedAP[0:q])

		if searchKey in clusterKeys:
			clusterIndex = clusterKeys.index(searchKey)
			clusterIndices.append(clusterIndex)
			locationCandidates.extend(clusterElements[clusterIndex])
		else:
			apLength = len(sortedAP)
			clusterKeysLength = len(clusterKeys)
			q += 1
			while q <= apLength:
				searchKey = set(sortedAP[0:q])

				for i in range(0, clusterKeysLength):
					if clusterKeys[i].issubset(searchKey):
						clusterIndices.append(i)
						locationCandidates.extend(clusterElements[i])

				if len(locationCandidates) > 0:
					break

				q += 1

		locationCandidates = list(set(locationCandidates))

		return status, clusterIndices, locationCandidates

	def computeLocationJointProbability(self, locationCandidate, rssiDict, log=False):
		probability = 0 if log else 1

		for apID in rssiDict:
			locationAP = self.radioMap[locationCandidate].get(apID, None)
			if locationAP:
				gaussianPrediction = round(dt.predictGaussian(rssiDict[apID], locationAP["mean"], locationAP["variance"]), 5)
				
				if gaussianPrediction > 1e-4:
					if log:
						probability += np.log(gaussianPrediction)
					else:
						probability *= gaussianPrediction

		return probability

	def predict(self, rssiResult, threshold=1.0):
		status = 0
		locationProbabilities = {}
		sortedLocationProbabilities = []

		rssiDict = dt.createRSSIDict(self.macDict, rssiResult)
		sortedAPs = self.sortedAP(rssiDict)

		status, clusterIndices, locationCandidates = self.findCluster(sortedAPs)
		
		if status != 0:
			status = 1
			return status, sortedLocationProbabilities

		for locationTag in locationCandidates:
			locationProbabilities[locationTag] = self.computeLocationJointProbability(locationTag, rssiDict)
		
		sortedLocationProbabilities = sorted(locationProbabilities.items(), key=lambda kv: kv[1], reverse=True)
		
		return status, sortedLocationProbabilities


class Model(ModelInterface):
	def __init__(self, paramsPath=None, debugMode=False):
		ModelInterface.__init__(self, paramsPath=None, debugMode=debugMode)
		self.horus = Horus()
		self.paramsPath = paramsPath
		
	def train(self, datasetPath, *args, **kwargs):
		if iu.isNone(self.horus.data):
			self.horus.loadDataset(datasetPath)
		self.horus.radioMapBuilder()
		self.horus.sortedAPRadioMap()
		self.horus.createClusters()
		if self.paramsPath:
			self.saveParameters()
		elif kwargs.get("paramsPath"):
			self.saveParameters(kwargs["paramsPath"])

	def predict(self, rssiResult):
		return self.horus.predict(rssiResult)

	def saveParameters(self, paramsPath=None):
		self.horus.saveParameters(self.paramsPath if self.paramsPath else paramsPath)
	
	def loadParameters(self, paramsPath=None):
		self.horus.loadParameters(self.paramsPath if self.paramsPath else paramsPath)