from xml.dom import minidom

def titleOfItem(item):
    return(item.getElementsByTagName('title')[0].firstChild.data)

tree = minidom.parse('example_feed.xml')

channel = tree.getElementsByTagName('channel')[0]

items = channel.getElementsByTagName('item')

for item in items:
    print("Title: "+str(titleOfItem(item)))
