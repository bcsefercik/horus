# -*- coding: utf-8 -*-

# Custom modules
from .RSSIKit import RSSIKit

from . import inlo_utils as iu

# Python built-in modules
import subprocess, re

# Python 3rd party libraries
import objc

class MacOSRSSIKit(RSSIKit):
	def __init__(self):
		RSSIKit.__init__(self)
		self.reMAC = re.compile(self.MACRegex)
		objc.loadBundle('CoreWLAN',
				bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
				module_globals=globals())

		self.interface= None
		for iname in CWInterface.interfaceNames():
			self.interface = CWInterface.interfaceWithName_(iname)
		
	def scanRSSI(self):
		# Status Code: 0->Success, 1->Error
		status_code = 0
		output = []
		try:
			if iu.isNone(self.interface):
				status_code = 2
				return status_code, None

			interfaceResults = self.interface.scanForNetworksWithChannels_ssid_bssid_error_(None,None,None,None)

			for ap in interfaceResults[0]:
				macAddress = ap.bssid().strip()
				if not macAddress:
					continue

				name = ap.ssid().strip()
				rssi = int(ap.rssi())
				channel = int(ap.channel())

				output.append({"name": name, "macAddress": macAddress, "rssi": rssi, "channel": channel})

		except Exception as e:
			print(e)
			status_code = 1

		return status_code, output
