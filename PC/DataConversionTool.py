# -*- coding: utf-8 -*-
import json
def convert(inp, labels, output):
	i = open(inp, 'r')
	l = open(labels, 'r')
	o = open(output, 'w')

	iContent = i.read().split("000000")
	lContent = l.read().strip().split('\n')
	

	ooo = []
	for ic in iContent:
		ll = ic.strip().split('\n')
		li = []  
		for lll in ll:
			lc = lll.split('\t')
			dd = {}
			dd["name"] = lc[0]
			dd["macAddress"] = lc[1]
			dd["rssi"] = lc[2]
			li.append(dd)

		ooo.append({"tag": int(lContent.pop(0)), "result": li})
	
	json.dump(ooo, o)

	i.close()
	l.close()
	o.close()

	return ooo

if __name__ == '__main__':
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument("-l", "--labels", type=str, default='in2.dat')
	ap.add_argument("-i", "--input", type=str, default='in.dat')
	ap.add_argument("-o", "--output", type=str, default='out.dat')
	opt = vars(ap.parse_args())
	convert(opt['input'], opt['labels'], opt['output'])
	