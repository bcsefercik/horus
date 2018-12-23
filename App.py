# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import threading
import datetime

import argparse
import importlib

from RSSIKitFactory import RSSIKitFactory, OSType
import inlo_utils as iu

DEBUG = True

factory = RSSIKitFactory()
kit = factory.getInstance(OSType.MACOS)

def filterData(resultList):
	# TODO: Gather mac list of mobile phones and stuff and filter.
	return resultList

def collect(datasetPath, tag, count=None, frequency=None, additionalInfo=None, ):
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

	returnCode, resultList, totalTime = kit.collectRSSI(tag = tag, frequency=frequency, count=count, additionalInfo=additionalInfo, debugMode=DEBUG)

	if returnCode != 0:
		iu.printLog("Code from RSSIKit.collectRSSI(): %d" % returnCode, debugMode=True, logType="error")
		statusCode = 1
		return statusCode

	filteredResultList = filterData(resultList)

	dataList.extend(resultList)

	with open(datasetPath, "w", encoding="utf-8") as json_file:
		json.dump(dataList, json_file, ensure_ascii=False, indent=2)

	return statusCode


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-task", "--task", type=str, default="")
	ap.add_argument("-tag", "--tag", type=str, default="")
	ap.add_argument("-data", "--datasetpath", type=str, default="result.json")
	ap.add_argument("-model", "--modelpath", type=str, default="")
	ap.add_argument("-params", "--modelparameterspath", type=str, default="")
	ap.add_argument("-count", "--count", type=int, default=100)
	ap.add_argument("-fq", "--frequency", type=int, default=20)
	ap.add_argument("-xinfo", "--additionalinfo", type=json.loads, default=None)
	ap.add_argument("-debug", "--debugmode", type=bool, default=False)
	opt = ap.parse_args()

	DEBUG = opt.debugmode

	if not opt.task:
		iu.printLog("Please run the app with '--task' parameter.\nOptions: collect, train, predict, validate.", logType="error")
	else:
		taskName = opt.task.lower()
		if taskName == "collect":
			if not (opt.datasetpath and opt.tag):
				iu.printLog("Missing paramaters.\nValid 'tag' and 'datasetpath' are required.", logType="error")
				sys.exit(1)
			
			if not os.path.isfile(opt.datasetpath):
				with open(opt.datasetpath, "w+", encoding='utf-8') as json_file:
					json.dump([], json_file, ensure_ascii=False, indent=2)

			collect(opt.datasetpath, opt.tag, count=opt.count, frequency=opt.frequency, additionalInfo=opt.additionalinfo)
		else:
			if not (opt.modelpath and os.path.isdir(opt.modelpath.replace(".", "/"))):
				iu.printLog("You need to provide a correct model path.", logType="error")
				sys.exit(1)

			if not opt.modelparameterspath:
				iu.printLog("Missing paramaters.\nValid 'modelparameterspath' is required.", logType="error")
				sys.exit(1)

			modelModulePath = opt.modelpath.replace("/", ".") + ".Model"
			module = importlib.import_module(modelModulePath)
			model = module.Model(opt.modelparameterspath, debugMode=DEBUG)

			if taskName == "train":
				if not (opt.datasetpath and os.path.isfile(opt.datasetpath)):
					iu.printLog("Missing paramaters.\nProper 'datasetpath' is required.", logType="error")
					sys.exit(1)

				if not os.path.isfile(opt.modelparameterspath):
					open(opt.modelparameterspath, 'w').close()
					iu.printLog("Model parameters file is created at {}.".format(opt.modelparameterspath))
				
				iu.printLog("Starting training with dataset at {}.".format(opt.datasetpath), debugMode=DEBUG)

				model.train(opt.datasetpath)

			elif taskName == "predict" or  taskName == "test":
				if not os.path.isfile(opt.modelparameterspath):
					iu.printLog("Missing paramaters.\nAn existing model parameters file at 'modelparameterspath' is required.", logType="error")
					sys.exit(1)

				keyboardEvent = threading.Event()

				iu.printLog("Starting prediction.")

				def getExitCommand():
					iu.printLog("You can write quit and press enter to stop predicting.")
					while not keyboardEvent.is_set():
						exitText = input("")
						if exitText.lower() == "quit":
							keyboardEvent.set()

				thread = threading.Thread(target=getExitCommand, args=())
				# If this thread is started, then one can take text inputs from the user in the terminal.
				# thread.start()

				period = 1 / opt.frequency
				
				while not keyboardEvent.is_set():
					startTime = time.time()
					
					statusCode, rssi = kit.scanRSSI()
					if statusCode:
						iu.printLog("RSSIKit.scanRSSI(): {}".format(statusCode), logType="error")
						keyboardEvent.set()
						sys.exit(1)

					statusCode, prediction = model.predict(rssi)
					if statusCode:
						iu.printLog("{}.predict(): {}".format(modelModulePath, statusCode), logType="error")
						keyboardEvent.set()
						sys.exit(1)

					iu.printLog("{}: {}".format(datetime.datetime.now(), prediction))

					iterationTime = time.time() - startTime
					time.sleep(max(0, period - iterationTime))

			elif taskName == "validate":
				# TODO
				pass

			else:
				iu.printLog("You should enter a valid task name.", logType="error")
				sys.exit(1)
