


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
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext , MessageHandler,Filters
from telegram import ParseMode
import re
import requests
from bs4 import BeautifulSoup
import time

from flask import Flask

app = Flask(__name__)

bot = Bot(token='YOUR-TOKEN')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

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

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    if update.message.from_user.id != 92203167:
        return 
    context.bot.send_message(chat_id=update.effective_chat.id, text="the scope bot starting at the channel") 
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if update.message.from_user.id != 92203167:
        return 
    update.message.reply_text('Help!')
    
def search(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == -1001573574395  and update.message.from_user.id == 777000  :
            message_id = update.message.message_id
            update_messege = update.message.text 
            link = update_messege[update_messege.find("https://rotter.net/forum/scoops1/")::]
            regex = r"""<!--<FONT CLASS='text16b'>-->(.*?)<!-- /69589285/Threads_Below_Main_Content -->"""
            f = requests.get(link)
            string = BeautifulSoup(f.content,features="lxml")
            for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
                sub_text = matchObj.group(0)
                sub_text = sub_text[sub_text.find("text15")::]
                sub_text = sub_text[sub_text.find("<br/>")::]
            soup = BeautifulSoup(sub_text, features="html.parser")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            string = '\n'.join(chunk for chunk in chunks if chunk)
            n = 2000 # chunk length
            chunks = [string[i:i+n] for i in range(0, len(string), n)]
            for mess in chunks:
                  if mess:
                    update.message.bot.send_message(chat_id=-1001573574395, text=mess, parse_mode = ParseMode.HTML ,reply_to_message_id = message_id)
                    time.sleep(0.2)
            images = soup.findAll('img')
            for image in images:
                context.bot.send_photo(chat_id=-1001573574395, photo=image['src'],reply_to_message_id = message_id)
    else : 
        return 

def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # its the RotterBot 
    updater = Updater(token='YOUR-TOKEN', use_context=True)
    # want put the test bot
    # updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start,run_async=True))
    dispatcher.add_handler(CommandHandler("help", help_command,run_async=True))
    dispatcher.add_handler(CommandHandler("test", search,run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
