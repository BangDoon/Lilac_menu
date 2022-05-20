import json 
import sys

import pandas as pd
import numpy as np

from datetime import date

from urllib.request import urlopen
from bs4 import BeautifulSoup

import os
from twilio.rest import Client

import schedule
import time

def this_week() :

  main = 'https://www.pknu.ac.kr/main/399'
  html = urlopen(main)  
  soup = BeautifulSoup(html, "html.parser") 
  hotKeys = soup.select("a")[199]['href']

  adr = f'{main}{hotKeys}'
  html = urlopen(adr)

  soup = BeautifulSoup(html, "html.parser") 
  hotKeys = soup.select("p")
  menu = []

  for t in hotKeys[28:93]:
    #print(t)
    a=str(t)[:89]
    #print(a)
    if(a=='<p style="margin: 0pt; word-break: keep-all; vertical-align: bottom; line-height: 130%;">'):
      #print(t)
      menu.append(t)

  week = [[], [], [], [], []]
  idx = 0
  before = 0
  for n,i in enumerate(menu) :

    

    if str(i)[-5] == '밥' and n !=0 and n - before > 3  :
      idx += 1
      before = n
      week[idx].append(str(i)[89:-4])
    
    else:
      week[idx].append(str(i)[89:-4])
    
  return week

def before_week() :

  main = 'https://www.pknu.ac.kr/main/399'
  html = urlopen(main)  
  soup = BeautifulSoup(html, "html.parser") 
  hotKeys = soup.select("a")[200]['href']

  adr = f'{main}{hotKeys}'
  html = urlopen(adr)

  soup = BeautifulSoup(html, "html.parser") 
  hotKeys = soup.select("p")
  menu = []

  for t in hotKeys[28:93]:
    #print(t)
    a=str(t)[:89]
    #print(a)
    if(a=='<p style="margin: 0pt; word-break: keep-all; vertical-align: bottom; line-height: 130%;">'):
      #print(t)
      menu.append(t)

  week = [[], [], [], [], []]
  idx = 0
  before = 0
  for n,i in enumerate(menu) :

    

    if str(i)[-5] == '밥' and n !=0 and n - before > 3  :
      idx += 1
      before = n
      week[idx].append(str(i)[89:-4])
    
    else:
      week[idx].append(str(i)[89:-4])

  return week

#twilo_setting 
account_sid = 'AC4a97b7b6a8bcead112bac3964e98d518'
auth_token = 'a303bc0955ecb9075536c1ff8131776f'
client = Client(account_sid, auth_token)

tit = ['Monday','Tuesday','Wednesday','Thursday','Friday']
#send message
def send_msg():
  
  
  today = date.weekday(date.today())

  if (today < 4):
    week = this_week()
    ms = f'****오늘의 라일락 메뉴****\n{str(week[today])[1:-1]}'

  elif(today==4):
    week = before_week()
    ms = f'****오늘의 라일락 메뉴****\n{str(week[today])[1:-1]}'

  if(today < 5):
    message = client.messages.create(
        to="+821041734742", 
        from_="+17755356857",
        body=ms)
  
    print('메세지 전송 완료')

#print(message.sid)

#set 주기
schedule.every().day.at("11:00").do(send_msg)


while True:
    schedule.run_pending()
    time.sleep(1)