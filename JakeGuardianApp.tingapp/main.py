import tingbot
from tingbot import *


import time
import os
import requests, json
from HTMLParser import HTMLParser

######################## GLOBALS ########################
state = {}
jsonResp = ''
webTitle = ''
webPublicationDate = ''
webUrl = ''
index = 0
######################## GLOBALS ########################

# make call
@every(minutes=5)
def get_data():

    req = requests.get('http://content.guardianapis.com/search?q=uk&api-key=9570cf30-7bc8-4683-8069-0cea7b060980')
    
    global jsonResp
    jsonResp = req.json()
    
    refresh_feed()
    
#parse content
def refresh_feed():
    global webTitle
    webTitle = HTMLParser().unescape(jsonResp['response']['results'][index]['webTitle'])


######################## BUTTONS ########################
@right_button.press
@left_button.press
def on_right():
    global index
    index = index +1
    refresh_feed()
    
@left_button.press
def on_left():
    global index
    index = index -2
    refresh_feed()

######################## BUTTONS ########################


@every(seconds=1.0/30)
def loop():
    # SETUP UI
    screen.fill(color='blue')
    screen.text(webTitle, color='white', font_size=16)

tingbot.run()
