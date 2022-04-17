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
from typing import Dict
from multiprocessing import Event
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
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

current_theather = None
current_movie = None
list_of_movies = None
user_posible = None
logger = logging.getLogger(__name__)

class user:
    def __init__(self,user_name,name) -> None:
        self.user_name = ''
        self.name = ''
        self.movie_availibe = {}
        
CHOOSEMOVIE,CHOOSEDATE,CALCULATEPOLL= range(3)

def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    keyboard = []
    button_list = []
    for key,value in cc_parser.theater.items():
        keyboard.append(InlineKeyboardButton(key,callback_data = value))
    button_list.append(keyboard)
    keyboard = button_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('בחר את בית הקולנוע הרצוי', reply_markup=reply_markup)
    return CHOOSEMOVIE

def choose_movie(update: Update, context: CallbackContext) -> int:
    global  current_theather
    global list_of_movies
    print('entor to choose theather')
    keyboard = []
    button_list = []
    query = update.callback_query
    query.answer()
    current_theather = query.data
    list_of_movies = cc_parser.get_theather_movies(query.data)
    for movie in list_of_movies:
        keyboard = list()
        keyboard.append(InlineKeyboardButton(movie.title[::-1],callback_data = movie.movieID))
        button_list.append(keyboard)
    keyboard = button_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('בחר את הסרט הרלוונטי', reply_markup=reply_markup)
    return CHOOSEDATE

def old_choose_date(update: Update, context: CallbackContext) -> int:
    global current_theather
    global list_of_movies
    print('entor to choose_date')
    keyboard = []
    button_list = []
    questions = []
    query = update.callback_query
    query.answer()
    current_movie = query.data
    for movie in list_of_movies:
        print(movie.movieID)
        if movie.movieID == query.data:
            for date in movie.date.keys():
                keyboard = list()
                keyboard.append(InlineKeyboardButton(date,callback_data = date))
                questions.append(date)
                button_list.append(keyboard)
        else:
            continue
    keyboard = button_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text('בחר את התאריך הרלוונטי', reply_markup=reply_markup)

def choose_date(update: Update, context: CallbackContext) -> int:
    print('entor to choose_date')
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
    print('enter to caluclate_poll')
    """Summarize a users poll vote"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        questions = context.bot_data[poll_id]["questions"]
    except: 
        return
    print(answer)
    print(questions)
    user = answer['user']
    ans = answer['option_ids']
    print(user['username'])
    print(user['last_name'] + ' ' + user['first_name'])
    print(ans)
    #print(answer['last_name'])
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