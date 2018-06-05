import os
from bs4 import BeautifulSoup
import requests
import pickle
import time
import subprocess
import signal
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

    for i in groups:
        with open('cachedsun/red/'+i,'w') as f:
            pro = subprocess.Popen(['grasp -fw 1 -d sun -g '+i], stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)
            s=' '
            resstr = ''
            while s:
                s=pro.stdout.readline()
                resstr +=s.decode('utf-8')
            f.write(resstr)
            #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    for i in groups:
            with open('cachedsun/blue/'+i,'w') as f:
                pro = subprocess.Popen(['grasp -fw 0 -d sun -g '+i], stdout=subprocess.PIPE,
                               shell=True, preexec_fn=os.setsid)
                s=' '
                resstr = ''
                while s:
                    s=pro.stdout.readline()
                    resstr +=s.decode('utf-8')
                f.write(resstr)
                #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    for i in groups:
            with open('cachedsun/full/'+i,'w') as f:
                pro = subprocess.Popen(['grasp -fd sun -g '+i], stdout=subprocess.PIPE,
                               shell=True, preexec_fn=os.setsid)
                s=' '
                resstr = ''
                while s:
                    s=pro.stdout.readline()
                    resstr +=s.decode('utf-8')
                f.write(resstr)
                #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
site()
print('End caching')
