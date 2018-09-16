# -*- coding: utf-8 -*-

# Custom modules
from RSSIKit import RSSIKit

import inlo_utils as iu

# Python built-in modules
import subprocess, re

class MacOSRSSIKit(RSSIKit):
	def __init__(self):
		RSSIKit.__init__(self)
		self.reMAC = re.compile(self.MACRegex)
		
	def scanRSSI(self):
		# Status Code: 0->Success, 1->Error
		status_code = 0
		output = []
		try:
			command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan".split(" ")
			result = subprocess.run(command, stdout=subprocess.PIPE)

			shell_output = result.stdout.decode("utf-8")
			shell_output_lines = shell_output.split("\n")

			if not shell_output_lines:
				status_code = 2
				return status_code, None

			shell_output_lines.pop(0)

			for line in shell_output_lines:
				line = iu.recursiveReplace(line, "  ", " ").strip()

				macAddress = self.reMAC.findall(line)
				if not macAddress:
					continue

				macAddress = macAddress[0]
				parts = line.split(macAddress)

				name = parts[0].strip()

				parts_right = (parts[1].strip()).split(" ")

				rssi = int(parts_right[0])
				channel = int((parts_right[1].split(","))[0])

				output.append({"name": name, "macAddress": macAddress, "rssi": rssi, "channel": channel})

		except:
			status_code = 1

		return status_code, output

	