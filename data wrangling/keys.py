#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re


def get_key(element):
    if element.tag=='tag':
        return element.attrib['k']


def process_map(filename):
    keys = dict()
    for _, element in ET.iterparse(filename):
        key=get_key(element)
        if key not in keys:
        	keys[key]=1
        else:
        	keys[key]+=1
    return keys

def get_unusual_keys(keys_dict):
	for key,value in keys_dict.items():
		if value>=5:
			del keys_dict[key]
	return keys_dict

def test():

    keys = process_map('bandung-samplek10.osm')
    pprint.pprint(keys)
    unusual_keys=get_unusual_keys(keys)
    pprint.pprint(unusual_keys)


if __name__ == "__main__":
    test()