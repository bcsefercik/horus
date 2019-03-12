# -*- coding: utf-8 -*-
import abc

class ModelInterface(abc.ABC):
	@abc.abstractmethod
	def __init__(self, paramsPath, debugMode=False):
		self.debugMode = debugMode
	
	@abc.abstractmethod
	def train(self, datasetPath):
		pass
		
	@abc.abstractmethod
	def predict(self, rssiResult):
		pass
		