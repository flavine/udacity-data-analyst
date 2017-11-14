import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#this script will use regex to see what street type that is present and
#check it against the expected street type

OSMFILE = "bandung-samplek10.osm"
street_type_re = re.compile(r'\S+\.?', re.IGNORECASE)
#\b\S+\.?$

expected_street_type = ["Jalan"] #the only street type in Indonesia


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types



def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    


if __name__ == '__main__':
    test()