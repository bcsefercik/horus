# -*- coding: utf-8 -*-
import abc

class ModelInterface(abc.ABC):
	def __init__(self, paramssPath, debugMode=False):
		self.paramssPath = paramssPath
		self.debugMode = debugMode
	
	@abc.abstractmethod
	def train(self, datasetPath):
		pass
		
	@abc.abstractmethod
	def predict(self, rssi):
		pass
	
