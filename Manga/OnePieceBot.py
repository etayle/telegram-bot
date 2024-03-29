
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
#!/usr/bin/python
from pydoc import text
import time
import re
import requests

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

dontAvaliabe = 'This Chapter is not available Yet. We will add it soon. When it Available'
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please choose chapter ! \n " + 
     'commands :+\n/chapter NumOfChapter \n/last to get last chapter available\n/sendlast to send the last chapters available')
    
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def sendlast(update: Update, context: CallbackContext) -> None :
    link = "https://www.onepiece-manga-online.net"
    f = requests.get(link)
    string = f.text
    soup = BeautifulSoup(string, "html.parser")
    string = f.text
    regex = r"""https:\/\/w[0-9]\.onepiece-manga-online\.net\/manga\/one-piece(-manga)?-chapter-[0-9]*?\/""";

    for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
        link = matchObj.group(0)
        print(link)
        f = requests.get(link)
        string = f.text
        soup = BeautifulSoup(string, "html.parser")
        if dontAvaliabe in string:
            continue
        textToSend = 'send chapter ' +  re.findall(r'\d+',link)[-1]
        context.bot.send_message(chat_id=update.effective_chat.id, text=textToSend)
        print(textToSend)
        regex = r"""(^<meta +property="og:image(?::url)?" +content="([^"]+)" *\/>$)""";
        intCount = 0

        for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
            try:
                print(matchObj.group(2))
                context.bot.send_photo(update.effective_chat.id, matchObj.group(2))
            except:
                errorMsg = 'failed occur when try send the img:\n' +  matchObj.group(2) 
                context.bot.send_message(chat_id=update.effective_chat.id, text=errorMsg)
        print('finish to send this chpater')
        return

def last(update: Update, context: CallbackContext) -> None :
    link = "https://www.onepiece-manga-online.net"
    f = requests.get(link)
    string = f.text
    soup = BeautifulSoup(string, "html.parser")
    string = f.text
    regex = r"""https:\/\/w[0-9]\.onepiece-manga-online\.net\/manga\/one-piece(-manga)?-chapter-[0-9]*?\/""";

    for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
        link = matchObj.group(0)
        print(link)
        f = requests.get(link)
        string = f.text
        soup = BeautifulSoup(string, "html.parser")
        if dontAvaliabe in string:
            continue
        dateModifed = soup.find("meta", {"property":"article:modified_time"})
        dateModifed = "-".join(dateModifed['content'].split('T')[0].split('-')[::-1])
        textToSend = 'Available chapter ' +  re.findall(r'\d+',link)[-1] + ' modifed at: ' +  dateModifed
        context.bot.send_message(chat_id=update.effective_chat.id, text=textToSend)
        print(textToSend)
        break
    
def chapter(update: Update, context: CallbackContext) -> None :
    link = "https://onepiece-manga-online.net/manga/one-piece-chapter-" + context.args[0] + '/'
    f = requests.get(link)
    string = f.text
    if dontAvaliabe in string:
        print("This chapter dont available")
        context.bot.send_message(chat_id=update.effective_chat.id, text="This chapter dont available")
        return
    #regex = r"""<ima?ge?(?=\s|>)(?=(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*?\ssrc=(['"]?)(.*?)\1(?:\s|>))(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*>""";
    regex = r"""(^<meta +property="og:image(?::url)?" +content="([^"]+)" *\/>$)""";
    intCount = 0
    for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
        print(matchObj.group(2))
        try:
            context.bot.send_photo(update.effective_chat.id, matchObj.group(2))
        except:
            continue
        time.sleep(0.2)
        intCount+=1
    context.bot.send_message(chat_id=update.effective_chat.id, text="Finish to send this chapter")
    print('finish to send this chpater')



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("chapter",chapter))
    dispatcher.add_handler(CommandHandler("last",last))
    dispatcher.add_handler(CommandHandler("sendlast",sendlast))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    main()
