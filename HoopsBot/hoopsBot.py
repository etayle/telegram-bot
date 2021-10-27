

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

from telegram import Update, ForceReply, message
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import re
import requests
from bs4 import BeautifulSoup
import time
from telegram import ParseMode


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
flag = True

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
    update.message.reply_text('the bot searching start')
    global flag
    flag = True
    regex = r"""<h2 class="blog-entry-title entry-title">(.*?)</h2><!-- .blog-entry-title -->"""
    link = "https://hoops.co.il/"
    last_scopse = []
    last_scopse_number = []
    if context.args and context.args[0].isnumeric():
        last_scopse_number.append(context.args[0])
        print(last_scopse_number[0])
    while flag:
            f = requests.get(link)
            string = BeautifulSoup(f.content)
            intCount =0
            for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
                if intCount == 5:
                    break
                title =matchObj.group(0)[matchObj.group(0).find("title="):matchObj.group(0).find('</a>'):].strip('title="').split('">')[0]
                link_of_scope = matchObj.group(0)[matchObj.group(0).find("https"):matchObj.group(0).find('" rel="bookmark"'):]
                link_of_scope_number = link_of_scope.split('=')[-1]
                print(link_of_scope_number)
                if link_of_scope_number in last_scopse_number:
                    break
                    #want to return to while 
                last_scopse_number.append(link_of_scope_number)
                last_scopse.append(title + '\n\n'  + 'קישור להודעה :' +'\n' + link_of_scope + '\n'  )
                intCount+=1
            for scopes in last_scopse[::-1]:
                    update.message.bot.send_message(chat_id=-1001292728001, text=scopes, parse_mode = ParseMode.HTML)
            last_scopse.clear()
            time.sleep(450)
    
def stop(update: Update, context: CallbackContext) -> None:
    global flag
    flag = 0
    update.message.reply_text('the bot stop')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='1988121128:AAEzMASC_64n9dZyXAf0XVAgStYcwdDQJIc', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start,run_async=True))
    dispatcher.add_handler(CommandHandler("help", help_command,run_async=True))
    dispatcher.add_handler(CommandHandler("search", search,run_async=True))
    dispatcher.add_handler(CommandHandler("stop", stop,run_async=True))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
