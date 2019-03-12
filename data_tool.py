# -*- coding: utf-8 -*-
import json
import numpy as np

import inlo_utils as iu

def convert(inp, labels, output):
	i = open(inp, 'r', encoding='utf-8')
	l = open(labels, 'r', encoding='utf-8')
	o = open(output, 'w', encoding='utf-8')

	iContent = i.read().split("000000")
	lContent = l.read().strip().split('\n')
	

	ooo = []
	for ic in iContent:
		ll = ic.strip().split('\n')
		li = []  
		for lll in ll:
			lc = lll.split('\t')
			dd = {}
			dd["name"] = lc[0]
			dd["macAddress"] = lc[1]
			dd["rssi"] = lc[2]
			li.append(dd)

		ooo.append({"tag": int(lContent.pop(0)), "result": li})
	
	json.dump(ooo, o, indent=2)

	i.close()
	l.close()
	o.close()

	return ooo

def createMacDict(inp, toFile = None):
	data = None
	if isinstance(inp, str):
		with open(inp) as f:
			data = json.load(f)
	else:
		data = inp

	macDict = {}

	for instance in data:
		for ap in instance["result"]:
			if not macDict.get(ap["macAddress"]):
				macDict[ap["macAddress"]] = len(macDict)

	if toFile:
		with open(toFile, "w") as of:
			json.dump(macDict, of, indent=2)

	return macDict


def analyseMacDict(inp, macDict=None, toFile=None):
	data = None
	if isinstance(inp, str):
		with open(inp) as f:
			data = json.load(f)
	else:
		data = inp

	if iu.isNone(macDict):
		macDict = createMacDict(inp)

	statDict = {}
	for instance in data:
		for ap in instance["result"]:
			if not statDict.get(ap["macAddress"]):
				statDict[ap["macAddress"]] = {	"id": macDict[ap["macAddress"]],
												"name": ap["name"],
											  	"locations": {instance["tag"]: [ap["rssi"]]}}
			else:
				if not statDict[ap["macAddress"]]["locations"].get(instance["tag"], None):
					statDict[ap["macAddress"]]["locations"][instance["tag"]] = [ap["rssi"]]
				else:
					statDict[ap["macAddress"]]["locations"][instance["tag"]].append(ap["rssi"])

	if toFile:
		with open(toFile, "w") as of:
			json.dump(statDict, of, indent=2)

	return statDict, macDict

def createHistogram(series):
	valueDict = {}

	for v in series:
		valueDict[v] = valueDict.get(v, 0) + 1

	valueDictSorted = dict(sorted(valueDict.items(), key=lambda kv: kv[0]))
	x = np.array(list(valueDictSorted.keys()))
	y = np.divide(list(valueDictSorted.values()), len(series))

	return x, y

def predictGaussian(x, mu, sigma2):
	# x: a numver or a number array
	return 1/(np.sqrt(2 * np.pi * sigma2) *np.exp( - (x - mu)**2 / (2 * sigma2) ) + 1e-30)

def createLocationRSSISeries(inp, toFile = None, macDict = None):
	status = 0
	data = None
	if isinstance(inp, str):
		with open(inp) as f:
			data = json.load(f)
	else:
		data = inp

	series = {}
	if iu.isNone(macDict):
		macDict = createMacDict(inp)
		if not macDict:
			status = 1
			return status, series

	for instance in data:
		tag = instance["tag"]
		if not series.get(tag):
			series[tag] = {}

		timestamp = instance.get("timestamp", 0)
		for ap in instance["result"]:
			apID = macDict[ap["macAddress"]]
			
			if not series[tag].get(apID):
				series[tag][apID] = {"rssiSeries": [], "timeSeries": []}

			series[tag][apID]["rssiSeries"].append(ap["rssi"])
			series[tag][apID]["timeSeries"].append(timestamp)

	for location in series:
		for ap in series[location]:
			if len(series[location][ap]["timeSeries"]) == 0:
				series[location][ap]["timeSeries"].clear()
				series[location][ap]["timeSeries"] = None

			series[location][ap]["mean"] = np.mean(series[location][ap]["rssiSeries"])
			series[location][ap]["variance"] = np.var(series[location][ap]["rssiSeries"])

	if toFile:
		with open(toFile, "w") as of:
			json.dump(series, of, indent=2)

	return status, series

def createRSSIDict(macDict, rssiResult):
	if iu.isNone(macDict):
		return {}
	return {macDict[ins["macAddress"]]: ins["rssi"] for ins in rssiResult if macDict.get(ins["macAddress"], False)}


if __name__ == '__main__':
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--task", type=str, default="convert")
	ap.add_argument("-l", "--labels", type=str, default=None)
	ap.add_argument("-i", "--input", type=str, default=None)
	ap.add_argument("-o", "--output", type=str, default=None)
	opt = ap.parse_args()

	taskName = opt.task.lower()
	if taskName == "convert" or taskName == "conversion":
		convert(opt.input, opt.labels, opt.output)
	elif taskName == "createmacdict" or taskName == "createbssiddict":
		createMacDict(opt.input, opt.output)
	