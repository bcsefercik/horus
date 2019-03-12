# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import data_tool as dt

from Models.Horus.Model import Horus,Model

horus = Horus()

horus.loadDataset("20181218-1730_ArcelikInnovationOffice.json")

s = horus.radioMapBuilder()

horus.sortedAPRadioMap()

# Desk5
sampleRSSIResult = [{"name": "arguest","macAddress": "00:62:ec:59:57:91","rssi": -60,"channel": 9},{"name": "test-pool","macAddress": "00:62:ec:59:57:9c","rssi": -55,"channel": 48},{"name": "arbyod","macAddress": "00:a6:ca:10:2e:5d","rssi": -42,"channel": 36},{"name": "arguest","macAddress": "84:3d:c6:f0:f7:ce","rssi": -89,"channel": 44},{"name": "arwifi","macAddress": "00:a6:ca:10:2e:50","rssi": -38,"channel": 13},{"name": "VRPGUEST","macAddress": "26:a4:3c:b1:6f:cf","rssi": -86,"channel": 36},{"name": "arwifi","macAddress": "00:a6:ca:10:2e:5f","rssi": -42,"channel": 36},{"name": "arbyod","macAddress": "00:a6:ca:10:2e:52","rssi": -34,"channel": 13},{"name": "FaceTracker","macAddress": "ec:08:6b:b7:4e:56","rssi": -51,"channel": 2},{"name": "test-pool","macAddress": "00:62:ec:59:57:93","rssi": -60,"channel": 9},{"name": "VRPGUEST","macAddress": "26:a4:3c:b2:6f:cf","rssi": -79,"channel": 1},{"name": "arbyod","macAddress": "00:62:ec:59:57:92","rssi": -60,"channel": 9},{"name": "arwifi","macAddress": "84:3d:c6:f0:f7:c0","rssi": -89,"channel": 9},{"name": "VRPWIFI","macAddress": "24:a4:3c:b1:6f:cf","rssi": -87,"channel": 36},{"name": "arguest","macAddress": "00:a6:ca:10:2e:5e","rssi": -42,"channel": 36},{"name": "arbyod","macAddress": "00:62:ec:59:57:9d","rssi": -55,"channel": 48},{"name": "SMGWIFI","macAddress": "00:1d:aa:60:5b:88","rssi": -78,"channel": 6},{"name": "test-pool","macAddress": "84:3d:c6:f0:f7:cc","rssi": -88,"channel": 44},{"name": "software_design_2.4GHZ","macAddress": "b0:4e:26:0a:35:f0","rssi": -88,"channel": 2},{"name": "arbyod","macAddress": "84:3d:c6:f0:f7:cd","rssi": -87,"channel": 44},{"name": "test-pool","macAddress": "84:3d:c6:f0:f7:c3","rssi": -89,"channel": 9},{"name": "arguest","macAddress": "00:a6:ca:10:2e:51","rssi": -38,"channel": 13},{"name": "arwifi","macAddress": "00:62:ec:59:57:9f","rssi": -54,"channel": 48},{"name": "VRPWIFI","macAddress": "24:a4:3c:b2:6f:cf","rssi": -79,"channel": 1},{"name": "HP-Print-86-LaserJet 200","macAddress": "08:3e:8e:8a:aa:86","rssi": -89,"channel": 6},{"name": "arbyod","macAddress": "84:3d:c6:f0:f7:c2","rssi": -90,"channel": 9},{"name": "test-pool","macAddress": "00:a6:ca:10:2e:53","rssi": -37,"channel": 13},{"name": "arguest","macAddress": "00:62:ec:59:57:9e","rssi": -55,"channel": 48},{"name": "tazi-guest","macAddress": "7a:8a:20:49:e2:22","rssi": -93,"channel": 11},{"name": "arwifi","macAddress": "84:3d:c6:f0:f7:cf","rssi": -88,"channel": 44},{"name": "arguest","macAddress": "84:3d:c6:f0:f7:c1","rssi": -89,"channel": 9},{"name": "test-pool","macAddress": "00:a6:ca:10:2e:5c","rssi": -42,"channel": 36},{"name": "arwifi","macAddress": "00:62:ec:59:57:90","rssi": -61,"channel": 9},{"name": "SMGGuest","macAddress": "02:1d:aa:60:5b:88","rssi": -80,"channel": 6}]

# Desk3
sampleRSSIResult = [{"name": "arwifi","macAddress": "00:a6:ca:10:2e:50","rssi": -39,"channel": 13},{"name": "arwifi","macAddress": "00:a6:ca:10:2e:5f","rssi": -47,"channel": 36},{"name": "HP-Print-86-LaserJet 200","macAddress": "08:3e:8e:8a:aa:86","rssi": -79,"channel": 6},{"name": "VRPGUEST","macAddress": "26:a4:3c:b2:6f:cf","rssi": -89,"channel": 1},{"name": "test-pool","macAddress": "84:3d:c6:f0:f7:cc","rssi": -88,"channel": 44},{"name": "arbyod","macAddress": "00:62:ec:59:57:92","rssi": -66,"channel": 9},{"name": "arbyod","macAddress": "00:a6:ca:10:2e:5d","rssi": -48,"channel": 36},{"name": "arguest","macAddress": "00:a6:ca:10:2e:5e","rssi": -48,"channel": 36},{"name": "arguest","macAddress": "00:a6:ca:10:2e:51","rssi": -44,"channel": 13},{"name": "arbyod","macAddress": "00:62:ec:59:57:9d","rssi": -68,"channel": 48},{"name": "test-pool","macAddress": "00:62:ec:59:57:93","rssi": -68,"channel": 9},{"name": "arguest","macAddress": "00:62:ec:59:57:9e","rssi": -68,"channel": 48},{"name": "test-pool","macAddress": "00:62:ec:59:57:9c","rssi": -67,"channel": 48},{"name": "test-pool","macAddress": "00:a6:ca:10:2e:53","rssi": -45,"channel": 13},{"name": "arwifi","macAddress": "00:62:ec:59:57:90","rssi": -66,"channel": 9},{"name": "arwifi","macAddress": "00:62:ec:59:57:9f","rssi": -68,"channel": 48},{"name": "test-pool","macAddress": "00:a6:ca:10:2e:5c","rssi": -47,"channel": 36},{"name": "arguest","macAddress": "00:62:ec:59:57:91","rssi": -67,"channel": 9},{"name": "arbyod","macAddress": "00:a6:ca:10:2e:52","rssi": -45,"channel": 13},{"name": "FaceTracker","macAddress": "ec:08:6b:b7:4e:56","rssi": -50,"channel": 2}]

sampleRSSIDict = dt.createRSSIDict(horus.macDict, sampleRSSIResult)

horus.createClusters(10,2)

horusModel = Model()
