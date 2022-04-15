

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
regex = r"""<h2 class="blog-entry-title entry-title">(.*?)</h2><!-- .blog-entry-title -->"""
link = "https://hoops.co.il/"
last_scopse = []
last_scopse_number = []
while True:
        f = requests.get(link)
        string = BeautifulSoup(f.content)
        intCount =0
        for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
            if intCount == 4:
                break

            title =matchObj.group(0)[matchObj.group(0).find("title="):matchObj.group(0).find('</a>'):].strip('title="').split('>')[0]
            print(title)
            link_of_scope = matchObj.group(0)[matchObj.group(0).find("https"):matchObj.group(0).find('" rel="bookmark"'):]
            link_of_scope_number = link_of_scope.split('=')[-1]
            if link_of_scope_number in last_scopse_number:
                time.sleep(15)
                break
                #want to return to while 
            last_scopse_number.append(link_of_scope_number)
            last_scopse.append(title + '\n\n'  + 'קישור להודעה :' +'\n' + link_of_scope + '\n'  )
            intCount+=1
        
