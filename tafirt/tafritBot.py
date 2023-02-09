import imp
import my_gmail


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
import os
dontAvaliabe = 'This Chapter is not available Yet. We will add it soon. When it Available'
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='hello my friend')
    
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
bot to get attachments from gmail: etayle10@gmail.com:
commands:
/send_last_photo: get the newst attachments the mail get in the last month
/send_photo_by_title arg_title
get the fist attachments to with specified title in the last month""")

def send_last_photo(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    is_valid, photo_path = my_gmail.get_my_email_last_attachment()
    if is_valid:
        print(photo_path)
        context.bot.send_photo(update.effective_chat.id, photo=open(photo_path,'rb') )
        os.remove(photo_path)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='not get a new attachment in the last month')

def send_photo_by_title(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if 0 < len(context.args):
        subject =  " ".join(context.args)
        is_valid, photo_path = my_gmail.get_my_email_attachment_by_title(subject)
        if is_valid:
            print(photo_path)
            context.bot.send_photo(update.effective_chat.id, photo=open(photo_path,'rb') )
            os.remove(photo_path)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='not get a new attachment in the last month')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='error: No argument given see /help for correct usage')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("send_last_photo", send_last_photo))
    dispatcher.add_handler(CommandHandler("send_photo_by_title", send_photo_by_title))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    main()
