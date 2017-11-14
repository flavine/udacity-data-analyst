import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "bandung-samplek10.osm"
postcodes_re = re.compile(r'\d{5}', re.IGNORECASE)
#\b\S+\.?$

expected = []


def audit_postcode(postcodes, postcode):
    m = postcodes_re.search(postcode)
    if m:
        postcode_number = m.group()
        if postcode_number not in expected:
            postcodes[postcode].add(postcode_number)



def is_postcode(elem):
    return (elem.attrib['k'] == 'addr:postcode')


def audit(osmfile):
    osm_file = open(osmfile, "r")
    postcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    audit_postcode(postcodes, tag.attrib['v'])
    osm_file.close()
    return postcodes



def test():
    postalcodes = audit(OSMFILE)
    pprint.pprint(dict(postalcodes))

    


if __name__ == '__main__':
    test()