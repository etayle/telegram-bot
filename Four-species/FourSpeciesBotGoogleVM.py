#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from os import PRIO_PGRP
import re
from typing import Dict

import gspread
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup, message, update
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    CallbackDataCache
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

gc = gspread.service_account(filename= '/home/itay_or_levi78/four-species-325810-093c62e6fccb.json')

sh = gc.open_by_key('1B5kqMI7IIHKCFgcvP2bbIXT03JDloynf_QYOQNphmt4').worksheet('w1')

logger = logging.getLogger(__name__)

CHOOSE,INSERTORDER,GETORDER,CITY,BUTTON,QUNTITY,NAME, ADDRESS, PHONE ,GET_NAME,GET_PHONE,COST,CHOOSE2= range(13)

order = ['city','name',[],[],'address','phone_number','cost']
cost = []


reply_keyboard = [
    ['הכנסת משלוח', 'קבלת פרטי משלוח']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

workbook_name = "/root/telegram_bot/Four-species/Orders.xlsx"

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    global order
    global cost
    order = ['city','name',[],[],'address','phone_number','cost']
    cost = []
    keyboard = [
        [
            InlineKeyboardButton("הכנסת משלוח למאגר", callback_data='1'),
        ],
        [InlineKeyboardButton("קבלת משלוח מהמאגר", callback_data='2'),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('בחר את הפעולה שאתה רוצה לבצע:', reply_markup=reply_markup)
    return CHOOSE

def choose(update: Update, context: CallbackContext) -> int:
    print('enter to choose')
    query = update.callback_query
    query.answer()
    if query.data == '1' :
        """Start the conversation and ask user for input."""
        keyboard = [
            [
                InlineKeyboardButton("אופקים", callback_data='אופקים'),
                InlineKeyboardButton("רחובות", callback_data='רחובות'),
            ],
            [InlineKeyboardButton("פטיש", callback_data='פטיש'), InlineKeyboardButton("בטחה", callback_data='בטחה'),],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('בחר את העיר של המשלוח:', reply_markup=reply_markup)
        return CITY
    elif query.data == '2':
        """Start the conversation and ask user for input."""
        keyboard = [
            [
                InlineKeyboardButton("שם פרטי ושם משפחה", callback_data='1'),
                InlineKeyboardButton("מספר פלאפון", callback_data='2'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text('בחר את דרך קבלת הפרטים של בעל המשלוח:', reply_markup=reply_markup)
        return GETORDER

def choose2(update: Update, context: CallbackContext) -> int:
    print('enter to choose2')
    query = update.callback_query
    query.answer()
    if query.data == '1' :
          return CITY
    elif query.data == '2':
        query.message.reply_text("הכנס שם פרטי ושם משפחה")
        return NAME



def city(update: Update, context: CallbackContext) -> int:
    print("i am at city handle")
    global order
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if order[0] == 'city':
      order[0] = query.data
    keyboard = [
        [
            InlineKeyboardButton("סט כשר 70", callback_data='70'),
            InlineKeyboardButton("סט מהודר 90", callback_data='90'),
        ],
        [InlineKeyboardButton("סט תמני 130", callback_data='130'), InlineKeyboardButton("בחירה חופשית- לא עובד", callback_data='erorr'),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("הכנס את סוג המשלוח", reply_markup=reply_markup)
    return BUTTON

def button(update: Update, context: CallbackContext) -> int:
    global order,cost
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    number = len(order[2])
    if query.data == '70':
        str_to_insert = str(number) + ' : ' + 'סט כשר 70'
    elif query.data == '90':
        str_to_insert = str(number) + ' : ' + 'סט מהודר 90'
    elif query.data == '130':
        str_to_insert = str(number) + ' : ' + 'סט תימני 130'
    if query.data.isnumeric():
       cost.append(int(query.data))
    order[2].append(str_to_insert)
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("אחר - עוד לא נתמך", callback_data='error'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('הכנס כמות של סטים', reply_markup=reply_markup)
    return QUNTITY

def quntity(update: Update, context: CallbackContext) -> int:
    global order
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    number = len(order[3])
    cost[-1] = int(cost[-1])*int(query.data)
    str_to_insert = str(number) + "->: " + query.data 
    order[3].append(str_to_insert)
    keyboard = [
        [
            InlineKeyboardButton("כן -לחץ פעמיים משום מה", callback_data='1'),
       
        ],[  InlineKeyboardButton("לא", callback_data='2'),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('האם אתה רוצה להכניס הזמנה נוספת על אותו שם', reply_markup=reply_markup)
    return CHOOSE2

def cost(update: Update, context: CallbackContext) -> int:
    global order
    print('enter to cost')
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    text = update.message.text
    order[6] = text
    update.message.reply_text("הכנס שם פרטי ושם משפחה")
    return NAME

def enter_name(update: Update, context: CallbackContext) -> int:
    global order
    order[6] = sum(cost)
    """Ask the user for info about the selected predefined choice."""
    print('enter to enter_name')
    text = update.message.text
    order[1] = text
    print('the name is ' + text)
    update.message.reply_text("הכנס כתובת")
    return ADDRESS

def get_address(update: Update, context: CallbackContext) -> int:
    global order
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    order[4] = text
    print('the address is: ' + text)
    update.message.reply_text("הכנס מספר פלאפון")
    return PHONE

def get_phone(update: Update, context: CallbackContext) -> None:
    global order
    text = update.message.text
    order[5] = text
    print('the phone is: ' + text)
    end()
    return ConversationHandler.END

def get_order(update: Update, context: CallbackContext) -> int:
    global order
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == '1':
        query.message.reply_text('הכנס שם פרטי ושם משפחה')
        return GET_NAME
    if query.data == '2':
        query.message.reply_text('הכנס מספר פלאפון')
        return GET_PHONE
     

def end():
    global order
    print(order)
    order[2] = "\n".join(order[2])
    order[3] = '\n'.join(order[3])
    sh.append_row(order)

def get_name_search(update: Update, context: CallbackContext) -> int:
    global order
    """Ask the user for info about the selected predefined choice."""
    sh = gc.open_by_key('1B5kqMI7IIHKCFgcvP2bbIXT03JDloynf_QYOQNphmt4').worksheet('w1')
    text = update.message.text
    max_rows = len(sh.get_all_values())
    find_row = None
    for row_numner in range(1,max_rows+1) :
        values_list = sh.row_values(1)
        for cell in sh.row_values(row_numner):
            if cell == text:
                find_row = sh.row_values(row_numner)
            else:
                continue
            break
    if find_row == None:
        update.message.reply_text("לא נמצא אדם עם המזהה הנ''ל")
    else:
        detiels = ""
        for data,amount in zip(find_row[2].split('\n'),find_row[3].split('\n')):
            detiels += str(data) + ', כמות: '+ str(amount[4::]) + '\n'
        replay_messege = "עיר: " + find_row[0] +'\n' + 'שם : ' + find_row[1] + '\n' +  detiels + '\n' + 'כתובת: ' + find_row[4] + '\n' + 'מספר פלאפון: ' + find_row[5] + '\n' + 'סך הכל לתשלום: ' + find_row[6]
        update.message.reply_text(replay_messege)
    return ConversationHandler.END

def get_phone_search(update: Update, context: CallbackContext) -> int:
    global order
    """Ask the user for info about the selected predefined choice."""
    sh = gc.open_by_key('1B5kqMI7IIHKCFgcvP2bbIXT03JDloynf_QYOQNphmt4').worksheet('w1')
    text = update.message.text
    max_rows = len(sh.get_all_values())
    find_row = None
    for row_numner in range(1,max_rows+1) :
        values_list = sh.row_values(1)
        for cell in sh.row_values(row_numner):
            if cell == text:
                find_row = sh.row_values(row_numner)
            else:
                continue
            break
    if find_row == None:
        update.message.reply_text("לא נמצא אדם עם המזהה הנ''ל")
    else:
        detiels = ""
        for data,amount in zip(find_row[2].split('\n'),find_row[3].split('\n')):
            detiels += str(data) + ', כמות: '+ str(amount[4::]) + '\n'
        replay_messege = "עיר: " + find_row[0] +'\n' + 'שם : ' + find_row[1] + '\n' +  detiels + '\n' + 'כתובת: ' + find_row[4] + '\n' + 'מספר פלאפון: ' + find_row[5] + '\n' + 'סך הכל לתשלום: ' + find_row[6]
        update.message.reply_text(replay_messege)
    return ConversationHandler.END
    


def done(update: Update, context: CallbackContext) -> None:
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='397823070:AAFAnRP2RwlpU_TC_QFnzhociPceODt6eus', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE: [
               CallbackQueryHandler(choose)
            ],
            CHOOSE2: [
               CallbackQueryHandler(choose2,pass_job_queue=True)
            ],
            CITY: [
               CallbackQueryHandler(city)
            ],
            GETORDER: [
               CallbackQueryHandler(get_order)
            ],
            BUTTON: [
               CallbackQueryHandler(button)
            ],
            QUNTITY: [
               CallbackQueryHandler(quntity)
            ],
            NAME: [
                MessageHandler(
                    Filters.text & ~Filters.command, enter_name
                ),
            ],
            ADDRESS: [
                MessageHandler(
                      Filters.text & ~Filters.command, get_address
                )
            ],
            PHONE: [
                MessageHandler(
                    Filters.text & ~Filters.command, get_phone,
                    PHONE,
                )
            ],
            GET_NAME: [
                MessageHandler(
                    Filters.text & ~Filters.command, get_name_search,
                    PHONE,
                )
            ],
            GET_PHONE: [
                MessageHandler(
                    Filters.text & ~Filters.command, get_phone_search,
                    PHONE,
                )
            ],
            COST: [
                MessageHandler(
                    Filters.text & ~Filters.command, cost,
                    PHONE,
                )
            ],   
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )
    dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()