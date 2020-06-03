# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 20:23:45 2019

@author: me
"""

import requests
import os

s = requests.Session()
headers = {
        "Host": "www.pythonanywhere.com",
        "User-Agent": os.environ['USR_AGENT'],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
        }
r = s.get("https://www.pythonanywhere.com/login/?next=/",headers=headers)

# Find the crfmiddlewaretoken
fulltext = r.text
try:
    searchstring = "csrfmiddlewaretoken' value='"
    start = fulltext.index(searchstring)
    end = fulltext.index("'",start + len(searchstring)+10)
    csrfmiddlewaretoken = fulltext[start+len(searchstring):end]
except:
    pass

data = {
        "csrfmiddlewaretoken":csrfmiddlewaretoken,
        "auth-username":os.environ['PA_USR'],
        "auth-password":os.environ['PA_PWD'],
        "login_view-current_step":"auth"
        }
headers = {
        "Host": "www.pythonanywhere.com",
        "User-Agent": os.environ['USR_AGENT'],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.pythonanywhere.com/login/?next=/",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }
# Login
r = s.post("https://www.pythonanywhere.com/login/?next=/",data=data,headers=headers,cookies=s.cookies)
if(r.status_code == 200):
    print("Succesful login!")

    headers = {
        "Host": "www.pythonanywhere.com",
        "User-Agent": os.environ['USR_AGENT'],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
        }
    r = s.get("https://www.pythonanywhere.com/user/{}/tasks_tab/".format(os.environ['PA_ACC']),headers=headers)
    #print(r.status_code)

    fulltext = r.text
    try:
        searchstring = 'Anywhere.csrfToken = "'
        start = fulltext.index(searchstring)
        end = fulltext.index('"',start + len(searchstring)+10)
        csrftoken = fulltext[start+len(searchstring):end]
    except:
        pass
    #print(csrftoken)

    headers = {
        "Host": "www.pythonanywhere.com",
        "User-Agent": os.environ['USR_AGENT'],
        "Accept": "application/json",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.pythonanywhere.com/user/{}/tasks_tab/".format(os.environ['PA_ACC']),
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
        "Origin": "https://www.pythonanywhere.com",
        "DNT": "1",
        "Connection": "keep-alive"
        }


    # Update task
    r = s.post("https://www.pythonanywhere.com/user/{}/schedule/task/{}/extend".format(os.environ['PA_ACC'],os.environ['PA_TASKNUM']),headers=headers,cookies=s.cookies)

    if(r.status_code == 200):
        print("Renewed task!")
    else:
        print("Failed at updating :(")

else:
    print("Can't login :(")
