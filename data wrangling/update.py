
from lxml import etree
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs

osmfile = "bandung-samplek10.osm"
street_type_re = re.compile(r'^\S+\.?', re.IGNORECASE)


street_mapping = { "Jl.": "Jalan",
            "JL": "Jalan",
            "JL.":"Jalan",
            "Jl.Kartini":"Jalan Kartini",
            "Jl.soekarno":"Jalan Soekarno"
            }

expected_street_type=['Jalan']


def update_street_name(street_mapping):
# if not in expected and if starts with Jl, will sub to Jalan
# if not, add Jalan
# remove hvhgvhghv
	outfile = codecs.open('updated_bandung.osm', 'w')
	tree=ET.iterparse(osmfile, events=("start",'end'))
	for event, elem in tree:
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if (tag.attrib['k'] == "addr:street"):
					name=tag.attrib['v']
					m=street_type_re.search(name)
					if m:
						street_type= m.group()
						if street_type=="hjvhj":
							tag.set('v','unknown')
							print ('street: hjvhj -> unknown')
						elif street_type not in expected_street_type and street_type in street_mapping:
							new_name = re.sub(street_type_re, street_mapping[street_type], name)
							tag.set('v',new_name)
							print ('street: ' +name + ' -> ' + new_name)
						elif street_type not in expected_street_type:
							new_name='Jalan '+ name
							tag.set('v',new_name)
							print('street: ' +name + ' -> ' + new_name)
	outfile.write(ET.tostring(elem, encoding='UTF-8'))
	outfile.close()



def update_user():
# update empty user and user id to anon and 000 if missing value
	osm_file="updated_bandung.osm"
	for event, elem in ET.iterparse(osm_file, events=("start",'end')):
		if elem.tag == "node" or elem.tag == "way":
			if 'user' not in elem.attrib and 'uid' not in elem.attrib:
					elem.set('user','anon')
					elem.set('uid','000')
					print ('user: None -> anon\n' + 'uid: None -> 000')
	outfile = codecs.open('updated_bandung.osm', 'w')
	outfile.write(ET.tostring(elem, encoding='UTF-8'))
	outfile.close()

key_mapping = { "Akreditasi": "accreditation",
            "food": "amenity:restaurant",
            "capacity:persons":"capacity:people",
            "capacity":"capacity:people", "Jml Rombel":"fixme",
            "lit":"fixme", "iata":"fixme","waktu belajar":"fixme",
            }

def update_keys(key_mapping):
# update or delete unusual keys in the osm file
# replace Jml Rombel, lit, iata, waktu belajar to fixme
# replace Akreditasi to accreditation (english translation)
# replace food to amenity:restaurant
# replace capacity and capacity:persons to capacity:people
# replace None keys to fixme

	osm_file="updated_bandung.osm"
	for event, elem in ET.iterparse(osm_file, events=("start",'end')):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if (tag.attrib['k'] in key_mapping):
					print ('key: ' + tag.attrib['k'] + ' -> ' + key_mapping[tag.attrib['k']])
					tag.set('k',key_mapping[tag.attrib['k']])
				elif tag.attrib['k']==None:
					tag.set('k','fixme')
					print ('key: None -> fixme')
	outfile = codecs.open('updated_bandung.osm', 'w')
	outfile.write(ET.tostring(elem, encoding='UTF-8'))
	outfile.close()

def test():
    update_street_name(street_mapping)
    update_keys(key_mapping)
    update_user()
    print ("Done updating street names, keys and users")
 

if __name__ == '__main__':
   	test()
