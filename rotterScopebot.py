

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



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    
    


def search_scope(update: Update, context: CallbackContext) -> None:
    """search for new scopes and send to the channel the user message."""
    if update.message.from_user.id != 92203167:
        return 
    link = "https://rotter.net/forum/listforum.php"
    regex = r"""<td align="right" valign="TOP" width="70%"><font class="text15bn" face="Arial"><a href=(.*?)</b></a>"""
    last_scopse = []
    last_scopse_number = []
    while True:
        f = requests.get(link)
        string = BeautifulSoup(f.content)
        intCount =0
        for matchObj in re.finditer( regex, string.encode().decode(), re.M|re.I|re.S):
            if intCount == 4:
                break
            #print(matchObj.group(0))
            link_of_scope = matchObj.group(0)[matchObj.group(0).find("https"):matchObj.group(0).find('" target'):]
            #print(link_of_scope)
            link_of_scope_number = int(link_of_scope.strip(".shtml").split('/')[5])
            #print(link_of_scope_number)
            if link_of_scope_number in last_scopse_number:
                time.sleep(5)
                break
                #want to return to while 
            last_scopse_number.append(link_of_scope_number)
            text = matchObj.group(0)[matchObj.group(0).find("<b>"):matchObj.group(0).find('</a>'):].strip('<b>').strip('</b>')
            last_scopse.append(text + '\n' + 'קישור לסקופ : ' + link_of_scope )
            intCount+=1
        for scopes in last_scopse[::-1]:
                update.message.bot.send_message(chat_id=-1001215937698, text=scopes)
        last_scopse.clear()



        

            



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_scope))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()