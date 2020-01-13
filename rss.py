#import xml.dom
from xml.dom import minidom
#from xml.etree import ElementTree as ET

def titleOfItem(item):
    return(item.getElementsByTagName('title')[0].firstChild.data)

tree = minidom.parse('example_feed.xml')

channel = tree.getElementsByTagName('channel')[0]

items = channel.getElementsByTagName('item')

for item in items:
    print("Title: "+str(titleOfItem(item)))

print("Let's add another post")
print("Title: ", end='')
title = input()
print("Description: ", end='')
description = input()

new_item = tree.createElement('item')
new_item_title = tree.createElement('title')
new_item_title.appendChild(tree.createTextNode(title))
new_item.appendChild(new_item_title)
new_item_desc = tree.createElement('description')
new_item_desc.appendChild(tree.createTextNode(description))
new_item.appendChild(new_item_desc)
channel.appendChild(new_item)

file = open('example_feed.xml', 'w')
tree.writexml(file)
print('Updated.')
#print(tree.toprettyxml())
