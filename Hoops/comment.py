
from typing import Counter
from matplotlib.pyplot import prism
import requests
from bs4 import BeautifulSoup
import pprint
def get_month(month):
    dict = {'אפר':4 , 'ינו':1, 'פבר':2, 'מרץ' : 3, 'מאי' : 5 , 'יונ':6, 'יול':7 , 'אוג':8, 'ספט':9, 'אוק':10 , 'נוב':11,'דצמ':12}
    try:
        return str(dict[month])
    except :
        print('error in get_month ')
def get_date(date):
    date = date.split()
    return date[0] +'.' + get_month(date[1]) + '.' + date[2]

class Comment:
    def __init__(self,comment) -> None:
        self.author = comment[2]
        self.date = get_date(comment[5])
        self.text = comment[11]
num = {}
link = "https://hoops.co.il/?p=262343"
f = requests.get(link)
soup = BeautifulSoup(f.content,features="html.parser")
for comment in soup.find_all('li' ,{'class': 'comment-container'}):
    comment= comment.find_all('div' ,{'class': 'comment-content'})[0].get_text().split('\n')
    c = Comment(comment)
    if num.get(c.author,None) == None:
        num[c.author] = 1
    else:
        num[c.author]+=1
pprint.pprint(num)
exit()
soup = soup.find_all('li' ,{'class': 'comment-container'})[0]
#print( soup.find_all('h3' ,{'class': 'comment-link'})[0].get_text())
#print( soup.find_all('span' ,{'class': 'comment-date'})[0].get_text().split())
s= soup.find_all('div' ,{'class': 'comment-content'})[0].get_text().split('\n')
c = Comment(s)
for ultag in soup.find_all('ul', {'class': 'market-block'}):
    # for litag in ultag.find_all('li'):
    for litag in ultag.select('li[class*="inlineItem inline-market inline-market"]'):
             print(str(Counter) + ': ',end=' ')
             print (litag )
             Counter+=1