# -*- coding: utf-8 -*-

def recursiveReplace(string, search, replace):
	if not (type(string) == str and type(search) == str and type(replace) == str):
		return None

	while search in string:
		string = string.replace(search, replace)

	return string
		