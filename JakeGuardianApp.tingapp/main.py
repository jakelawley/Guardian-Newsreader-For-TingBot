import tingbot
from tingbot import *

import os
import requests, json
from HTMLParser import HTMLParser

# make call

@every(minutes=10)
def refresh_data():

    req = requests.get('http://content.guardianapis.com/search?q=technology&api-key=9570cf30-7bc8-4683-8069-0cea7b060980')
    
    resp = req.json()
    
    headline1 = HTMLParser().unescape(resp['response']['results'][0]['sectionName'])

    screen.text(headline1, color='blue', font_size=16)    








@every(seconds=1.0/30)
def loop():
    # drawing code here
    screen.fill(color='black')
    
    refresh_data()

tingbot.run()
