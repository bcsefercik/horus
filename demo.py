# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import data_tool as dt



def predictGaussian(x, mu, sigma2):
	return 1/np.sqrt(2 * np.pi * sigma2) *np.exp( - (x - mu)**2 / (2 * sigma2) )



def plotRSSI(node):
	X = node["rssiSeries"]
	mu = node["mean"]
	sigma2 = node["variance"]
	
	count, bins, ignored = plt.hist(X, 30, density=True)

	plt.plot(bins, predictGaussian(bins, mu, sigma2),linewidth=2, color='r')

	plt.show()


s, a = dt.createLocationRSSISeries("EngineeringBuilding_20170501.json", toFile="EngineeringBuilding_20170501_RadioMap.json")

