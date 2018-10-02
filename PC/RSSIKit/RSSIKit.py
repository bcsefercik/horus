# -*- coding: utf-8 -*-

import time, datetime

COLLECT_RSSI_DEFAULTS = {"frequency": 20, "period": 3, "duration": 300, "count": 100}

class RSSIKit():
	global COLLECT_RSSI_DEFAULTS

	def __init__(self):
		self.MACRegex = r'(?:[0-9a-fA-F]:?){12}'

	def scanRSSI(self, returnType):
		# To be implemented in subclasses.
		raise NotImplementedError

	def collectRSSI(self, tag=None, frequency=COLLECT_RSSI_DEFAULTS["frequency"], period=COLLECT_RSSI_DEFAULTS["period"], count=COLLECT_RSSI_DEFAULTS["count"], duration=COLLECT_RSSI_DEFAULTS["duration"], **kwargs):
		# frequency: int 1/s
		# period: int s
		# duration: int s
		# count: 100 int number of iterations

		totalTimeStart = time.time()
		status_code = 0

		if frequency != COLLECT_RSSI_DEFAULTS["frequency"]:
			period = round(60/frequency)

		period = max(3, period)

		if count == COLLECT_RSSI_DEFAULTS["count"] and duration != COLLECT_RSSI_DEFAULTS["duration"]:
			count = round(duration/period)

		result = []


		while len(result) < count:
			requestTime = time.time()
			timestamp = datetime.datetime.fromtimestamp(requestTime).strftime('%Y-%m-%d %H:%M:%S')			

			scanResult = self.scanRSSI()
			if scanResult[0] != 0:
				status_code = 1
				break

			instanceResult = {"tag": tag, "result": scanResult[1], "timestamp": timestamp}
			
			for key, val in kwargs.items():
				instanceResult[key] = val

			result.append(instanceResult)

			finishTime = time.time()
			time.sleep(max(0.3, (period-(finishTime-requestTime))))

		totalTime = time.time() - totalTimeStart

		return status_code, result, totalTime
		