# -*- coding: utf-8 -*-

from ..ModelInterface import ModelInterface

import inlo_utils as iu


class Model(ModelInterface):
	"""docstring for Model"""
	def __init__(self, paramsPath, debugMode=False):
		ModelInterface.__init__(self, paramsPath, debugMode=debugMode)
		
	def train(self, datasetPath):
		pass

	def predict(self, rssi):
		return 0,2
