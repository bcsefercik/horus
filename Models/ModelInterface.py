# -*- coding: utf-8 -*-
import abc

class ModelInterface(abc.ABC):
	def __init__(self, paramsPath, debugMode=False):
		self.paramsPath = paramsPath
		self.debugMode = debugMode
	
	@abc.abstractmethod
	def train(self, datasetPath):
		pass
		
	@abc.abstractmethod
	def predict(self, rssi):
		pass
	
