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
import json
import logging
from os import PRIO_PGRP
from typing import Dict
from multiprocessing import Event
import requests
from bs4 import BeautifulSoup
import re
from telegram import(
    ReplyKeyboardMarkup,
    Update,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    message,
    update,
    Poll
    ) 
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    CallbackDataCache,
    PollAnswerHandler,
    PollHandler
)
import cc_parser

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

list_of_movies = []
dict_of_movies = {}
current_theather = None
current_movie = None
list_of_movies = None
user_posible = None
user_dict ={}

def intersect(a, b):
    d = {}
    for i in a:
        if i in b :
            lst3 = [value for value in a[i] if value in b[i]]
            d[i] = lst3
    return d

class User:
    def __init__(self,user_name,name) -> None:
        self.user_name = user_name
        self.name = name
        self.movie_availibe = {}
    

CHOOSEMOVIE,CHOOSEDATE,CALCULATEPOLL= range(3)

def start(update: Update, context: CallbackContext) -> int:
    keyboard = []
    button_list = []
    for key,value in cc_parser.theater.items():
        keyboard = list()
        keyboard.append(InlineKeyboardButton(key,callback_data = value))
        button_list.append(keyboard)
    keyboard = button_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('בחר את בית הקולנוע הרצוי', reply_markup=reply_markup)
    return CHOOSEMOVIE

def choose_movie(update: Update, context: CallbackContext) -> int:
    global current_theather
    global list_of_movies
    global dict_of_movies
    keyboard = []
    button_list = []
    query = update.callback_query
    query.answer()
    current_theather = query.data
    if not list_of_movies  :
        list_of_movies = cc_parser.get_theather_movies(query.data)
    for movie in list_of_movies:
        keyboard = list()
        keyboard.append(InlineKeyboardButton(movie.title[::-1],callback_data = movie.movieID))
        button_list.append(keyboard)
        dict_of_movies[movie.movieID] = movie.title[::-1]
    keyboard = button_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('בחר את הסרט הרלוונטי', reply_markup=reply_markup)
    return CHOOSEDATE

def choose_date(update: Update, context: CallbackContext) -> int:
    global current_movie
    questions = []
    query = update.callback_query
    query.answer()
    current_movie = query.data
    for movie in list_of_movies:
        if movie.movieID == query.data:
            for date in movie.date.keys():
                questions.append(date)
        else:
            continue
    message = context.bot.send_poll(
        update.effective_chat.id,
        "בחר את התאריכים האפשריים",
        questions,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    return CALCULATEPOLL

def caluclate_poll(update: Update, context: CallbackContext) -> int:
    global user_posible
    user_date = []
    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        questions = context.bot_data[poll_id]["questions"]
    except: 
        print('throw exception in caluclate_poll')
        return ConversationHandler.END
    user = answer['user']
    user_name = user['username']
    ans = answer['option_ids']
    if user_dict.get(user_name,None) == None:   
        c = User(user['username'],user['last_name'] + ' ' + user['first_name'])
        user_dict[user_name] = c
    current_user = user_dict[user_name]
    for i in ans:
        user_date.append(questions[i])
    current_user.movie_availibe[(current_theather,current_movie)] = user_date
  
    return ConversationHandler.END

def get(update: Update, context: CallbackContext) -> None:
    print('enter to get')
    for user,value in user_dict.items():
        print(user)
        print(value.movie_availibe)
    return ConversationHandler.END

def avd(update: Update, context: CallbackContext) -> None:
    if len(user_dict) == 0:
        return
    cur_dict = list(user_dict.values())[0].movie_availibe
    for user,value in user_dict.items():
        cur_dict = intersect(cur_dict,value.movie_availibe)
    for key,value in cur_dict.items():
        message = cc_parser.theater_id_to_name[key[0]] + ' : ' + dict_of_movies[key[1]] + ' : ' + str(value) + '\n'
    update.message.reply_text(message)

def test(update: Update, context: CallbackContext) -> None:
    if len(user_dict) == 0:
        return
    user_dict['test'] = user_dict[list(user_dict.keys())[0]]
    user_dict.pop(list(user_dict.keys())[0],None)
    print(user_dict)
    
def reset(update: Update, context: CallbackContext) -> None:
    global list_of_movies
    list_of_movies = []
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
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('get',get),
            CommandHandler('reset',reset),
            CommandHandler('avd',avd),
            CommandHandler('test',test),
            ],
        states={
            CHOOSEMOVIE: [
               CallbackQueryHandler(choose_movie)
            ], 
            CHOOSEDATE: [
               CallbackQueryHandler(choose_date)
            ], 
            CALCULATEPOLL: [
               PollAnswerHandler(caluclate_poll)
            ], 
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(PollAnswerHandler(caluclate_poll))
    
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()