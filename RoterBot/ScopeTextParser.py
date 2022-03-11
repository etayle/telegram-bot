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
def get_chunks(s, maxlength):
    start = 0
    end = 0
    while start + maxlength  < len(s) and end != -1:
        end = s.rfind(" ", start, start + maxlength + 1)
        yield s[start:end]
        start = end +1
    yield s[start:]
    
def replace_all(text, l):
    for i in l:
        text = text.replace(i, "")
    return text
from flask import Flask

link = "https://rotter.net/forum/scoops1/721353.shtml"
regex = r"""<!--<FONT CLASS='text16b'>-->(.*?)<!-- /69589285/Threads_Below_Main_Content -->"""
f = requests.get(link)
string = BeautifulSoup(f.content,features="lxml")
list_of_remove = ["<p>","<br/>","</p>","</b>"]
for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
     sub_text = matchObj.group(0)
     sub_text = sub_text[sub_text.find("text15")::]
     sub_text = sub_text[sub_text.find("<br/>")::]
soup = BeautifulSoup(sub_text, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out
for link in soup.find_all('a', href=True):
    print(link['href'])
images = soup.findAll('img')
for image in images:
    print(image['src'])
# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
n = 2000 # chunk length
chunks = [text[i:i+n] for i in range(0, len(text), n)]
for mess in chunks:
        print(mess)
