import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import numpy as np
from io import BytesIO
import requests
from pprint import pprint

raw = pd.read_json('cards.json')
cardarr = raw['data'].values

##
# define a simple search function that uses list comprehensions
def search(cat, text, output, flag=0):
    # if flag = 1, exact match, else, flag = 0, text is contained in cat
    # uses lower case!!!!
    if flag == 1:
        return [card[output] for card in cardarr if cat in card.keys() if output in card.keys() if card[cat].lower() == text.lower() ]
    else:
        return [card[output] for card in cardarr if cat in card.keys() if output in card.keys() if text.lower() in card[cat].lower() ]

##
# find out which cards were loeft our of core2
coreset = set( search('pack_code', 'core', 'title', 1) )
core2set = set( search('pack_code', 'core2', 'title', 1) )
# rotated cards from core
print(coreset - core2set)
# new cards in core2 (from first two cycles)
print('\n')
print(core2set - coreset)

##
# print a specific card, if available
#urls=search('title','death','image_url',0)
urls=search('title','rewiring','image_url',0)
if len(urls) > 0:
    for url in urls:
        #url = urls[0]
        plt.figure(figsize = (5,6))
        response = requests.get(url)
        img = mpimg.imread(BytesIO(response.content))

        imgplot = plt.imshow(img,interpolation='bilinear')
        plt.show()
else:
    print('\nImage not available\n')


## 
cards = [card for card in cardarr if 'accel' in card['title'].lower()]
# plot a card
for card in cards:
#plt.figure()
    height = 418
    width = 300
    
    #plt.axis('equal')
    fig = plt.figure(figsize = (4,5))
    ax = plt.gca()
    ax.set_position([0,0,1,1])
    ax.set_ybound(lower = 0, upper = height)
    ax.set_xbound(lower = 0, upper = width)
    
    if 'title' in card.keys():
        plt.text(0.05*width,0.5*height,card['title'],wrap=True, fontsize=14)
    if 'type_code' in card.keys():
        plt.text(0.05*width,0.55*height,card['type_code'].upper(),wrap=True, fontsize=12)
    if 'advancement_cost' in card.keys():
        plt.text(0.9*width,0.9*height,card['advancement_cost'],wrap=True, fontsize=16)
    if 'agenda_points' in card.keys():
        plt.text(0.05*width,0.6*height,card['agenda_points'],wrap=True, fontsize=16)
    if 'text' in card.keys():
        plt.text(0.05*width,0.45*height,card['text'],wrap=True, fontsize=12,verticalalignment='top')
    if 'flavor' in card.keys():
        plt.text(0.05*width,0.15*height,card['flavor'],wrap=True, fontsize=8)
    if 'cost' in card.keys():
        plt.text(0.05*width,0.9*height,card['cost'], fontsize=16)
    if 'faction_cost' in card.keys():
        plt.text(0.05*width,0.05*height,card['faction_cost'])
    if 'faction_code' in card.keys():
        plt.text(0.3*width,0.05*height,card['faction_code'])
    if 'trash_cost' in card.keys():
        plt.text(0.95*width,0.05*height,card['trash_cost'])
    
plt.show()

##
