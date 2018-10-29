# -*- coding: utf-8 -*-

from enum import Enum, unique

@unique
class OSType(Enum):
	UBUNTU = 0
	MACOS = 1
	WINDOWS = 2

class RSSIKitFactory():
	def __init__(self, OS=OSType.MACOS):
		pass

	def getInstance(self, OS):
		if OS == OSType.UBUNTU:
			from UbuntuRSSIKit import UbuntuRSSIKit
			return UbuntuRSSIKit()
		elif OS == OSType.MACOS:
			from RSSIKit.MacOSRSSIKit import MacOSRSSIKit
			return MacOSRSSIKit()
		elif OS == OSType.WINDOWS:
			from WindowsRSSIKit import WindowsRSSIKit
			return WindowsRSSIKit()


		