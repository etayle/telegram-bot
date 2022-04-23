from multiprocessing import Event
import requests
from bs4 import BeautifulSoup
import re
import pandas
from selenium import webdriver
import pprint

regex = r"""[\u0590-\u05FF\uFB1D-\uFB4F]+""";
theater = {'גלילות':'1170', 'ראשל"צ' :'1173' , 'ירושלים' :'1174', 'כפר-סבא' :'1175' , 'נתניה' :'1176' , 'באר שבע' :'1178' , 'חדרה' :'1350' , 'אשדוד' :'1181'}
theater_id_to_name = {'1170':'גלילות', '1173' :'ראשל"צ' , '1174' :'ירושלים', '1175' :'כפר-סבא' , '1176' :'נתניה' , '1178' :'באר שבע' , '1350' :'חדרה' , '1181' :'אשדוד'}

class Movie:
    def __init__(self,title,date,movieID) -> None:
        self.title = title 
        self.date = date
        self.movieID = movieID

def parse_event(link,movieID):
    dict_date= {}
    f = requests.get(link)
    soup = BeautifulSoup(f.content,features="html.parser")
    movie = f.json()[0]
    for event in movie['Dates']:
        date = event['Date'].split()[0] 
        hour = event['Hour'] 
        if dict_date.get(date,None) == None:
            set_of_hours = list()
            set_of_hours.append(hour)
            dict_date[date] = set_of_hours
        else:
            dict_date[date].append(hour)
    return Movie(movie['Name'][::-1],dict_date,movieID)
        
def parse_link(link):
    f = requests.get(link)
    soup = BeautifulSoup(f.content,features="html.parser")
    title = ""
    for word in soup.find_all('h1' ,{'class': 'col d-inline-flex title'}):
        for matchObj in list(re.finditer( regex, str(word), re.M|re.I|re.S))[::-1]:
            title += matchObj.group(0)[::-1] + " "

def get_theather_movies(theatherID):
    link = "https://www.cinema-city.co.il"
    f = requests.get(link)
    soup = BeautifulSoup(f.content,features="html.parser")
    ret_list = []
    for movie in soup.find_all('div' ,{'class': 'hide-on-desktop'}):
        try:
            link_site_movie = movie.find_all('a' ,href = True)[0]['href']
            img_movie = movie.find_all('img')[0]['src']
            if 'www' in link_site_movie and 'https' in img_movie:
                movieID = re.findall(r'\d+',link_site_movie)[0]
                link_to_movie = "https://www.cinema-city.co.il/tickets/Events?TheatreId=" + theatherID + '&VenueTypeId=1&MovieId=' + movieID + "&Date=0"
                ret_list.append(parse_event(link_to_movie,movieID))
        except:
            pass
    return ret_list

    