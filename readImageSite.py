#!/usr/bin/python
import re
import requests

link = "https://onepiece-manga-online.net/manga/one-piece-chapter-1/"
f = requests.get(link)

string = f.text

regex = r"""<ima?ge?(?=\s|>)(?=(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*?\ssrc=(['"]?)(.*?)\1(?:\s|>))(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*>""";

intCount = 0

for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
    print("[", intCount, "][ 2 ] : ", matchObj.group(2))
    intCount+=1