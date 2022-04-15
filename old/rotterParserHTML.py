

#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python

# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import time

from telegram import message

#string = f.text
#print(string.encode().decode())
#regex = r""";<b>(.*?)</b></a></font></TD>""";
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
            print(link_of_scope)
            link_of_scope_number = int(link_of_scope.strip(".shtml").split('/')[5])
            #print(link_of_scope_number)
            if link_of_scope_number in last_scopse_number:
                time.sleep(5)
                break
                #want to return to while 
            last_scopse_number.append(link_of_scope_number)
            text = matchObj.group(0)[matchObj.group(0).find("<b>"):matchObj.group(0).find('</a>'):].strip('<b>').strip('</b>')
            last_scopse.append(text + '\n\n' + 'קישור לסקופ : ' + link_of_scope + ' <a href="http://www.example.com/">קישור למובייל</a>'  )
            intCount+=1
        for scopes in last_scopse[::-1]:
                update.message.bot.send_message(chat_id=-1001292728001, text=scopes, parse_mode = ParseMode.HTML)
        last_scopse.clear()