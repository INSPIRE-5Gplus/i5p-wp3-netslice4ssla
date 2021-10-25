#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

import xml.etree.ElementTree as ET

#XML content is parse to a tree structure and its ROOT is retrieved
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()

## READING XML DOCUMENTS
# one specific item attribute
print('Item #2 attribute:')
print(root[0][1].attrib)

# all item attributes
print('\nAll attributes:')
for elem in root:
    for subelem in elem:
        print(subelem.attrib)

# one specific item's data
print('\nItem #2 data:')
print(root[0][1].text)

# all items data
print('\nAll item data:')
for elem in root:
    for subelem in elem:
        print(subelem.text)

# count total amount of items
print('\nCounting the XML elements:')
print(len(root[0]))

## WRITING XML DOCUMENTS
# create the file structure
data = ET.Element('data')
items = ET.SubElement(data, 'items')
item1 = ET.SubElement(items, 'item')
item2 = ET.SubElement(items, 'item')
item1.set('name','item1')
item2.set('name','item2')
item1.text = 'item1abc'
item2.text = 'item2abc'

# create a new XML file with the results
mydata = ET.tostring(data)
myfile = open("xml_text/items2.xml", "w")
myfile.write(str(mydata))


## FINDING XML ELEMENTS
# find the first 'item' object
print("\nFind the first 'item' object.")
for elem in root:
    print(elem.find('item').get('name'))

# find all "item" objects and print their "name" attribute
print("\nFind all the 'item' objects.")
for elem in root:
    for subelem in elem.findall('item'):
        # if we don't need to know the name of the attribute(s), get the dict
        print(subelem.attrib)      
        # if we know the name of the attribute, access it directly
        print(subelem.get('name'))

## MODIFYING XML ELEMENTS
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()

# changing a field text
for elem in root.iter('item'):
    elem.text = 'new text'

# modifying an attribute
for elem in root.iter('item'):
    elem.set('name', 'newitem')

# adding an attribute
for elem in root.iter('item'):
    elem.set('name2', 'newitem2')

tree.write('xml_text/newitems.xml')

##CREATING XML SUB-ELEMENTS
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()

# adding an element to the root node
attrib = {}
element = root.makeelement('seconditems', attrib)
root.append(element)

# adding an element to the seconditem node
attrib = {'name2': 'secondname2'}
subelement = root[0][1].makeelement('seconditem', attrib)
ET.SubElement(root[1], 'seconditem', attrib)
root[1][0].text = 'seconditemabc'

# create a new XML file with the new element
tree.write('xml_text/newitems2.xml')

##DELETING XML ELEMENTS
#### Removing an attribute
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()
# removing an attribute
root[0][0].attrib.pop('name', None)
# create a new XML file with the results
tree.write('xml_text/newitems3.xml')
#### Removing a sub-element
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()
# removing one sub-element
root[0].remove(root[0][0])
# create a new XML file with the results
tree.write('xml_text/newitems4.xml')
#### Removing al sub-elements
tree = ET.parse('xml_text/items.xml')
root = tree.getroot()
# removing all sub-elements of an element
root[0].clear()
# create a new XML file with the results
tree.write('xml_text/newitems5.xml')