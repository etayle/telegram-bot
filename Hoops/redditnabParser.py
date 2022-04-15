

#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Bot,Update, ForceReply, message
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import ParseMode
import re
import requests
from bs4 import BeautifulSoup
import time

from flask import Flask
regex = r"""class="_3jOxDPIQ0KaOWpzvSQo-1s" data-click-id="timestamp" href="(.*?)</h3></div></a></div><div class="_1hLrLjnE1G_RBCNcN9MVQf">"""
link = "https://www.reddit.com/r/nba/top/?t=day"
last_scopse = []
last_scopse_number = []
while True:
        f = requests.get(link)
        string = BeautifulSoup(f.content)
        intCount =0
        for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
            if intCount == 3:
                exit()
            link = matchObj.group(0).replace ('class="_3jOxDPIQ0KaOWpzvSQo-1s" data-click-id="timestamp" href="',"")
            link = link[:link.find('" rel'):]
            text = matchObj.group(0)[matchObj.group(0).find('><h3 class="_eYtD2XCVieq6emjKBH3m"')::].replace('</h3></div></a></div><div class="_1hLrLjnE1G_RBCNcN9MVQf">',"").replace('eYtD2XCVieq6emjKBH3m">',"")
            text = text.replace('><h3 class="_',"")
            print(text + '\n' + link + '\n')
            intCount+=1
        
