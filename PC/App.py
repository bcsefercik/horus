# -*- coding: utf-8 -*-

from RSSIKitFactory import RSSIKitFactory, OSType


factory = RSSIKitFactory(OSType.MACOS)
kit = factory.getInstance()

scanned = kit.scanRSSI()

print(kit.collectRSSI(tag=1, count=2))