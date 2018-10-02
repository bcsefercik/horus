# -*- coding: utf-8 -*-
import argparse

from RSSIKitFactory import RSSIKitFactory, OSType

def collectData():
	pass

factory = RSSIKitFactory(OSType.MACOS)
kit = factory.getInstance()

scanned = kit.scanRSSI()

print(kit.collectRSSI(tag=1, count=2))



if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--task", type=str, default='predict')
	ap.add_argument("-s", "--slots", type=str, default='@location_to=üsküdar,istanbul')
	ap.add_argument("-l", "--language", type=str, default='TR')
	opt = vars(ap.parse_args())