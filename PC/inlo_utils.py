# -*- coding: utf-8 -*-

def recursiveReplace(string, search, replace):
	if not (type(string) == str and type(search) == str and type(replace) == str):
		return None

	while search in string:
		string = string.replace(search, replace)

	return string
	

def printLog(text, debugMode=True, logType="info", title=True):
	# TODO: Indentation should same for every line of the message.
	logTypes = ["info", "ok", "warning", "error"]
	titles = {"info": "INFO", "ok": "SUCCESS", "warning": "WARNING", "error": "ERROR"}
	colors = {"ok": "\033[92m", "warning": "\033[93m", "error": "\033[91m"}
	endc = "\033[0m"

	if isinstance(logType, int): 
		if logType >= len(logTypes):
			return -1

		logType = logTypes[logType]
	else:
		if not logType in logTypes:
			return -1

	if title:
		text = titles[logType] + ": " + text

	if logType != "info":
		text = colors[logType] + text + endc

	if debugMode:
		print(text)

	return 0