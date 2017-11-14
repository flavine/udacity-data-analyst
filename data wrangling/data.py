#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "bandung-samplek10.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    update_street_name(element)
    update_keys(element)
    update_user(element)

    if element.tag=='node':
        for attr in element.attrib:
            if attr in node_attr_fields:
                node_attribs[attr]=element.attrib[attr]
    if element.tag=='way':
        for attr in element.attrib:
            if attr in way_attr_fields:
                way_attribs[attr]=element.attrib[attr]
        counter=0
        for nd in element.iter('nd'):
            way_node={}
            way_node['id']=way_attribs['id']
            way_node['node_id']=nd.attrib['ref']
            way_node['position']=counter
            counter+=1
            way_nodes.append(way_node)
    for tag in element.iter('tag'):
        tag_attribs={}
        if not problem_chars.search(tag.attrib['k']):
            if LOWER_COLON.search(tag.attrib['k']):
                splitter=tag.attrib['k'].split(':',1)
                tag_attribs['type']=splitter[0]
                tag_attribs['key']=splitter[1]
            else:
                tag_attribs['type']=default_tag_type
                tag_attribs['key']=tag.attrib['k']
            tag_attribs['value']=tag.attrib['v']
            tag_attribs['id']=element.attrib['id']
            tags.append(tag_attribs)
            
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def update_street_name(elem):
# if not in expected and if starts with Jl, will sub to Jalan
# if not, add Jalan
# remove hvhgvhghv
    street_type_re = re.compile(r'^\S+\.?', re.IGNORECASE)


    street_mapping = { "Jl.": "Jalan",
            "JL": "Jalan",
            "JL.":"Jalan",
            "Jl.Kartini":"Jalan Kartini",
            "Jl.soekarno":"Jalan Soekarno"
            }

    expected_street_type=['Jalan']
    
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


def update_user(elem):
# update empty user and user id to anon and 000 if missing value
    if elem.tag == "node" or elem.tag == "way":
        if 'user' not in elem.attrib and 'uid' not in elem.attrib:
                elem.set('user','anon')
                elem.set('uid','000')
                print ('user: None -> anon\n' + 'uid: None -> 000')


def update_keys(elem):
# update or delete unusual keys in the osm file
# replace Jml Rombel, lit, iata, waktu belajar to fixme
# replace Akreditasi to accreditation (english translation)
# replace food to amenity:restaurant
# replace capacity and capacity:persons to capacity:people
# replace None keys to fixme
    
    key_mapping = { "Akreditasi": "accreditation",
            "food": "amenity:restaurant",
            "capacity:persons":"capacity:people",
            "capacity":"capacity:people", "Jml Rombel":"fixme",
            "lit":"fixme", "iata":"fixme","waktu belajar":"fixme",
            }
    
    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if (tag.attrib['k'] in key_mapping):
                print ('key: ' + tag.attrib['k'] + ' -> ' + key_mapping[tag.attrib['k']])
                tag.set('k',key_mapping[tag.attrib['k']])
            elif tag.attrib['k']==None:
                tag.set('k','fixme')
                print ('key: None -> fixme')


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
