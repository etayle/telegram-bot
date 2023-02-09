from multiprocessing import Event
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pprint
from datetime import date, timedelta
import json


Books=["", "יהושע", "שופטים", "שמואל", "מלכים", "ישעיהו", "ירמיהו", "יחזקאל", "תרי עשר", "תהילים", "משלי", "איוב", "שיר השירים", "רות", "איכה", "קהלת", "אסתר", "דניאל", "עזרא ונחמיה", "דברי הימים"]
hebNumClean=["", "א'", "ב'", "ג'", "ד'", "ה'", "ו'", "ז'", "ח'", "ט'", "י'", "יא", "יב", "יג", "יד", "טו", "טז", "יז", "יח", "יט", "כ'", "כא", "כב", "כג", "כד", "כה", "כו", "כז", "כח", "כט", "ל'", "לא", "לב", "לג", "לד", "לה", "לו", "לז", "לח", "לט", "מ'", "מא", "מב", "מג", "מד", "מה", "מו", "מז", "מח", "מט", "נ'", "נא", "נב", "נג", "נד", "נה", "נו", "נז", "נח", "נט", "ס'", "סא", "סב", "סג", "סד", "סה", "סו", "סז", "סח", "סט", "ע'", "עא", "עב", "עג", "עד", "עה", "עו", "עז", "עח", "עט", "פ'", "פא", "פב", "פג", "פד", "פה", "פו", "פז", "פח", "פט", "צ" ];

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
# (year, month, day)
def getSeder(single_date):
    link = "https://www.tanachyomi.co.il/getDateInfo2?gd={day}&gm={month}&gy={year}&s=".format(day=single_date.strftime("%d"), month = single_date.strftime("%m"), year = single_date.strftime("%Y") )
    f = requests.get(link)
    html  = BeautifulSoup(f.content,features="html.parser")
    jsonData = json.loads(html.text) 
    link2 = "https://he.m.wikisource.org/wiki/" +  Books[int(jsonData['sederBook'])] + "/" + "סדר_"  + hebNumClean[int(jsonData['sederPart'].split(".")[0])].replace("'","")
    f = requests.get(link2)
    soup  = BeautifulSoup(f.content,features="html.parser")
    string = f.text
    regex = r"""parser-output"><section class="mf-section-0" id="mf-section-0"><center>\n<p>(.*)<\/p><p><a""";
    for matchObj in re.finditer( regex, string, re.M|re.I|re.S|re.DOTALL):
        link = matchObj.group(1)
        return link