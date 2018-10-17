# -*- coding: utf-8 -*-
import os
import json

import argparse

from RSSIKitFactory import RSSIKitFactory, OSType
import inlo_utils as iu

DEBUG = True

factory = RSSIKitFactory()
kit = factory.getInstance(OSType.MACOS)

def filterData(resultList):
	# TODO: Gather mac list of mobile phones and stuff and filter.
	return resultList

def collectData(datasetPath, tag, count=None, frequency=None, additionalInfo=None):
	statusCode = 0
	dataList = None

	if os.path.isfile(datasetPath):
		with open(datasetPath, encoding='utf-8') as json_file:
			dataList = json.load(json_file)

		iu.printLog("Loaded an existing dataset.", DEBUG)
	else:
		dataList = []
		iu.printLog("Created a new dataset.", DEBUG)

	iu.printLog("Starting to collect data.", DEBUG)

	returnCode, resultList, totalTime = kit.collectRSSI(tag = tag, frequency=frequency, count=count, additionalInfo=additionalInfo)

	if returnCode != 0:
		iu.printLog("Code from RSSIKit.collectRSSI(): %d" % returnCode, debugMode=True, logType="error")
		statusCode = 1
		return statusCode

	filteredResultList = filterData(resultList)

	dataList.extend(resultList)

	with open(datasetPath, "w", encoding="utf-8") as json_file:
		json.dump(dataList, json_file, ensure_ascii=False, indent=2)

	return statusCode

	



# scanned = kit.scanRSSI()

# print(kit.collectRSSI(tag=1, count=2))






if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--task", type=str, default=None)
	ap.add_argument("-s", "--slots", type=str, default='@location_to=üsküdar,istanbul')
	ap.add_argument("-l", "--language", type=str, default='TR')
	opt = vars(ap.parse_args())

	if not opt["task"]:
		iu.printLog("Please run the app with 'task' parameter.\nOptions: ", logType="error")
	else:
		taskName = opt["task"].lower()
		if taskName == "collect":
			if not (opt["datasetPath"] and opt["tag"]):
				pass
			collectData("ab.dat", 1, count=1)
