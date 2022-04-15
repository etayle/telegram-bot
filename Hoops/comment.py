#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email import header
import imp
import re
from typing import Counter
import requests
from bs4 import BeautifulSoup
import json
import locale
import time
import pandas as pd
import openpyxl
class Author:
     def __init__(self,name) -> None:
         self.author = name
         self.num_of_post = 1
         
class Comment:
    def __init__(self,comment) -> None:
        self.author = comment[2]
        try:
            self.date = Date(comment[5],comment)
        except:
            self.date = Date(comment[4],comment)
        self.text = comment[11]

class Golesh:
    def __init__(self,name,date) -> None:
        self.author = name
        self.num_of_comments = 0
        self.num_of_words = 0 
        self.last_date_respond = date
    def __repr__(self):
            return [self.num_of_comments,self.num_of_words,self.last_date_respond]
    def __str__(self) :
       return str([self.num_of_comments,self.num_of_words,self.last_date_respond])
class Date:
    def __init__(self,date,coment) -> None:
        date = date.split()
        self.day = date[0]
        self.month = get_month(date[1])
        self.year = date[2]
    def __repr__(self) -> str:
        return str(self.day) + '.' + str(self.month) + '.' + str(self.year)
    def __str__(self) -> str:
        return str(self.day) + '.' + str(self.month) + '.' + str(self.year)

def get_month(month):
    dict = {'אפר':4 , 'ינו':1, 'פבר':2, 'מרץ' : 3, 'מאי' : 5 , 'יונ':6, 'יול':7 , 'אוג':8, 'ספט':9, 'אוק':10 , 'נוב':11,'דצמ':12}
    try:
        return str(dict[month])
    except :
        print('error in get_month ')

def get_most_use_word():
    set_of_words = set()
    link = 'https://1000mostcommonwords.com/1000-most-common-hebrew-words/'
    f = requests.get(link)
    string = f.text
    regex = r"""[\u0590-\u05FF\uFB1D-\uFB4F]+""";
    intCount = 0
    for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
        set_of_words.add(matchObj.group(0))
    return set_of_words

def get_all_links(page_number):
    link = 'https://hoops.co.il/?paged=' + str(page_number)
    f = requests.get(link)
    string = f.text
    regex = r"""<a href="(.*?)" class="thumbnail-link">""";
    intCount = 0
    s=  re.findall(regex,string)
    return s

def parse_link(link):
    f = requests.get(link)
    soup = BeautifulSoup(f.content,features="html.parser")
    for comment in soup.find_all('li' ,{'class': 'comment-container'}):
        comment= comment.find_all('div' ,{'class': 'comment-content'})[0].get_text().split('\n')
        c = Comment(comment)
        if users.get(c.author,None) == None:
            current_user = Golesh(c.author,c.date)
            users[c.author] = current_user
        else:
            current_user = users[c.author]
        current_user.num_of_comments += 1
        current_user.num_of_words += len(c.text.split())
        for i in c.text.split():
            if i not in most_used :
                if words_count.get(i,None) == None:
                    words_count[i] = 1
                else:
                    words_count[i]+=1

def parse_page(page_number):
    print('parse page: ' + str(page_number))
    start_time = time.time()
    all_links= get_all_links(page_number)
    for link in all_links:
        parse_link(link)
    print("--- %s seconds ---" % (time.time() - start_time))

most_used = get_most_use_word()
users = {}
words_count = {}
for i in range(1,64):
    try:
        parse_page(i)
    except:
        print('error occur in page: ' + str(i) )
users={k: v for k, v in sorted(users.items(), key=lambda item: item[1].num_of_comments)}
w={k: v for k, v in sorted(words_count.items(), key=lambda item: item[1])}


with pd.ExcelWriter('data.xlsx') as writer:  
    w = pd.DataFrame(data=w, index=[0])
    w = (w.T)
    w.to_excel(writer,sheet_name='word')

    users = pd.DataFrame(data=users, index=[0])
    users = (users.T)
    users.to_excel(writer,sheet_name='users')


