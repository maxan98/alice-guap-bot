import os
from bs4 import BeautifulSoup
import requests
import pickle
import time
def site():

    r = requests.get("http://rasp.guap.ru/").content.decode('utf-8')
    soups = BeautifulSoup(r, "html.parser")
    select = soups.findAll('option')
    values = []
    groups = []
    for i in range (1,len(select)):
        if 'нет' in select[i].text:
            break
        values.append(select[i]['value'])
        groups.append(select[i].text)
    for i in range(len(values)):
    	r = requests.get("http://rasp.guap.ru/?g="+values[i]).content.decode('utf-8')
    	f = open('/root/cached/'+groups[i],'w')
    	f.write(r)
    	f.close()
    	lol = time.localtime(time.time())
    	with open (os.path.expanduser('~/cached/'+groups[i]+'.pkl'),'wb') as f:
    		pickle.dump(lol,f)

site()
print('End caching')
