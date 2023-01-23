
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
from datetime import date, timedelta
import tanachParser
from telegram import Update, ForceReply
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="welcome to etay bot! now we print TANACH")

def sendSeder(update, context):
    #2023-01-31
    start_date = date(2023, 1, 23)
    end_date = date(2023, 2, 1)
    for single_date in tanachParser.daterange(start_date, end_date):
        time.sleep(1)
        print(single_date)
        text = tanachParser.getSeder(single_date)
        if text == None:
            continue
        text = "\n".join(text.split(",")).replace('סדר ', '', 1)
        context.bot.send_message(chat_id=-1001826874463, text=text, parse_mode = ParseMode.HTML)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    sendSeder
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sendSeder", sendSeder))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    main()
