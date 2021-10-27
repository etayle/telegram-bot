
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
import re
import requests

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    print('enter to start')
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please choose chapter ! \n command : /chapter NumOfChapter")
    
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def chapter(update: Update, context: CallbackContext) -> None :
    #link = "https://onepiece-manga-online.net/manga/one-piece-chapter-" + context.args[0] + "/"
    link = "https://onepiece-manga-online.net/manga/one-piece-chapter-1029/"
    f = requests.get(link)

    string = f.text

    regex = r"""<ima?ge?(?=\s|>)(?=(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*?\ssrc=(['"]?)(.*?)\1(?:\s|>))(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*>""";

    intCount = 0
    print(context.args[0])
    for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
        context.bot.send_photo(update.effective_chat.id, matchObj.group(2))
        intCount+=1


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

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()