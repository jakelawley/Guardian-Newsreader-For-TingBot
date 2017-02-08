import tingbot
from tingbot import *

import time
import os
import requests, json
from HTMLParser import HTMLParser

######################## GLOBALS ########################
sections = ['uk','politics','world','sport','football','opinion','culture','business','lifestyle','fashion','enviroment','tech','travel','money','science']
currentSection = 'sectionNameHere'
jsonResp = ''
webTitle = ''
webPublicationDate = ''
webUrl = ''
resultsIndex = 0
sectionsIndex = 0
######################## GLOBALS ########################

# make call
@every(minutes=5)
def get_data():

    global currentSection
    currentSection = sections[int(sectionsIndex)]

    req = requests.get('http://content.guardianapis.com/search?q=' + currentSection + '&api-key=9570cf30-7bc8-4683-8069-0cea7b060980')
    
    global jsonResp
    jsonResp = req.json()
    
    refresh_feed()
    
#parse content
def refresh_feed():
    global webTitle
    webTitle = HTMLParser().unescape(jsonResp['response']['results'][resultsIndex]['webTitle'])


######################## BUTTONS ########################
@right_button.press
@left_button.press
def on_right():
    global sectionsIndex
    sectionsIndex = int(sectionsIndex + 1)
    get_data()
    
@left_button.press
def on_left():
    global sectionsIndex
    sectionsIndex = int(sectionsIndex - 2)
    get_data()

######################## BUTTONS ########################

@every(seconds=1.0/30)
def loop():
    # SETUP UI
    screen.fill(color=(0,86,137))
    screen.text(webTitle, color='white', font_size=16, xy=(160, 50), align='top', max_lines=2, max_width=260)
    screen.text(currentSection,align='topleft', xy=(5,5), font_size=12)

tingbot.run()
