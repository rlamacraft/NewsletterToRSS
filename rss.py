from xml.dom import minidom
from datetime import datetime

def titleOfItem(item):
    return(item.getElementsByTagName('title')[0].firstChild.data)

def get_tree(filename):
    return(minidom.parse(filename))
    
def get_channel(tree):
    channel = tree.getElementsByTagName('channel')[0]
    return(channel)

def print_item_titles(channel):
    items = channel.getElementsByTagName('item')
    for item in items:
        print("Title: "+str(titleOfItem(item)))

def day(datetime):
    day_map = {
        0: "Sun"
      , 1: "Mon"
      , 2: "Tue"
      , 3: "Wed"
      , 4: "Thu"
      , 5: "Sat"
      , 6: "Sun"
      }
    return(day_map[datetime.weekday()])

def month(datetime):
    month_map = {
        0 : "Jan",
        1 : "Feb",
        2 : "Mar",
        3 : "Apr",
        4 : "May",
        5 : "Jun",
        6 : "Jul",
        7 : "Aug",
        8 : "Sep",
        9 : "Oct",
        10: "Nov",
        11: "Dec"
    }
    return(month_map[datetime.month])
        
def formatted_now():
    now = datetime.now()
    return(f'{day(now)}, {now.day} {month(now)} {now.year} {now.hour}:{now.minute}:{now.second} +0000')
        
def append_new_item(tree, channel):
    print("Let's add another post")
    print("Title: ", end='')
    title = input()
    print("Description: ", end='')
    description = input()

    num_of_existing_items = len(tree.getElementsByTagName('item'))
    
    new_item = tree.createElement('item')
    new_item_title = tree.createElement('title')
    new_item_title.appendChild(tree.createTextNode(title))
    new_item.appendChild(new_item_title)
    new_item_desc = tree.createElement('description')
    new_item_desc.appendChild(tree.createTextNode(description))
    new_item.appendChild(new_item_desc)
    new_item_guid = tree.createElement('guid')
    new_item_guid.appendChild(tree.createTextNode('https://raw.githubusercontent.com/rlamacraft/NewsletterToRSS/master/feed.xml#'+str(num_of_existing_items+1)))
    new_item.appendChild(new_item_guid)
    new_item_pubDate = tree.createElement('pubDate')
    new_item_pubDate.appendChild(tree.createTextNode(formatted_now()))
    new_item.appendChild(new_item_pubDate)
    channel.appendChild(new_item)
    return(tree)

def write_xml(filename, tree):
    file = open(filename, 'w')
    tree.writexml(file)
    print('Updated.')

filename = 'example_feed.xml'    
tree = get_tree(filename)
channel = get_channel(tree)
print_item_titles(channel)
new_tree = append_new_item(tree, channel)
write_xml(filename, tree)



