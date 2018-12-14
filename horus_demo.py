# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import data_tool as dt

from Models.Horus.Model import Horus

horus = Horus("a.dat")

horus.loadDataset("EngineeringBuilding_20170501.json")

s, radioMap = horus.radioMapBuilder()
 