import tingbot
from tingbot import *

import time
import datetime
import os
import requests, json
from HTMLParser import HTMLParser

######################## GLOBALS ########################
sections = ['uk','politics','world','sport','football','opinion','culture','business','lifestyle','fashion','enviroment','tech','travel','money','science']
currentSection = ''
jsonResp = ''
webTitle = ''
webPublicationDateFormatted = ''
webUrl = ''
resultsIndex = 0
sectionsIndex = 0
######################## GLOBALS ########################

# make call
@every(minutes=15)
def get_data():

    global currentSection
    currentSection = sections[int(sectionsIndex)]
    
    apiKey = tingbot.app.settings['ApiKey']
    pageSize = tingbot.app.settings['PageSize']
    
    req = requests.get('http://content.guardianapis.com/search?q=' + currentSection + '&order-by=newest&page-size=' + str(pageSize) + '&api-key=' + apiKey)
    
    global jsonResp
    jsonResp = req.json()
    
    refresh_feed()
    
#parse content
def refresh_feed():
    global webTitle
    webTitle = HTMLParser().unescape(jsonResp['response']['results'][resultsIndex]['webTitle'])
    
    pubDateRaw = HTMLParser().unescape(jsonResp['response']['results'][resultsIndex]['webPublicationDate'])
    global webPublicationDateFormatted
    webPublicationDateFormatted = pubDateRaw
    #webPublicationDateFormatted = datetime.datetime.strptime(pubDateRaw, "%Y-%m-%d %H:%M:%S")
    
    global webUrl
    webUrl = HTMLParser().unescape(jsonResp['response']['results'][resultsIndex]['webUrl'])

######################## BUTTONS ########################
@right_button.press
def on_right():
    global resultsIndex
    pageSize = tingbot.app.settings['PageSize']
    if (resultsIndex+1) > (int(pageSize)-1):
        resultsIndex = resultsIndex
    else:
        resultsIndex = resultsIndex +1
    
    refresh_feed()
    
@left_button.press
def on_left():
    global resultsIndex
    if (resultsIndex-1) < 0:
        resultsIndex = resultsIndex
    else:
        resultsIndex = resultsIndex -1
    
    refresh_feed()
    
@midleft_button.press
def on_midleft():
    global resultsIndex
    resultsIndex = 0
    global sectionsIndex
    if(sectionsIndex < 1):
        get_data()
    else:
        sectionsIndex = int(sectionsIndex - 1)
        get_data()
    
@midright_button.press
def on_midright():
    numOfSections = len(sections)
    global resultsIndex
    resultsIndex = 0
    global sectionsIndex
    if((sectionsIndex+2) > numOfSections): 
        get_data()
    else:
        sectionsIndex = int(sectionsIndex + 1)
        get_data()
    
######################## BUTTONS ########################

@every(seconds=1.0/30)
def loop():
    # SETUP UI
    screen.brightness = 100
    screen.fill(color=(0,86,137))
    screen.text(webTitle, color='white', font_size=17, xy=(160, 50), align='top', max_lines=5, max_width=320)
    screen.text(currentSection,align='topleft', xy=(5,5), font_size=13)
    pageSize = tingbot.app.settings['PageSize']
    screen.text(str(resultsIndex+1) + ' of ' + str(pageSize), align='topright', font_size=13, xy=(310,5))
    screen.text('Published - ' + webPublicationDateFormatted, color='white', align='bottom', font_size=13)

tingbot.run()
