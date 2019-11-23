import os
import re
import time
import sys
from os import listdir
from os.path import isfile, join

import pyautogui as py

wait_time = int(sys.argv[1])
scorlling = True

filename = './../USA.txt'

def getwebList(filename):
  weblist = []
  with open (filename,'r') as file:
    for line in file:
      weblist.append(line.replace('\n',''))
    file.close()
    return weblist

def cross_check_list(url_list):
  # entries = os.listdir('./..')
  mypath = './website_data'
  entries = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  new_list = []
  # print url_list[1]
  for url in url_list:
    for f in entries:
      if url.lower() in f:
        # print url.lower(),'  ',f
        new_list.append(url)
  new_list = list(set(new_list)) #removing the duplicates
  # print new_list,'\n\n\n\n',url_list
  for f in new_list:
    url_list.remove(f)
  return url_list


def run_automation(url_list):
      for url in url_list:
    # py.click(706,107) #clear the log
    py.click(569,76) #click url bar
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite(str(url)) #enter url
    py.press("enter") #press enter
    time.sleep(wait_time) #wait for the website to load
    if scorlling == True: #perform scrolling if enabled
      py.moveTo(384,312)
      py.scroll(-30) #takes as argument number of pixels to scroll
      time.sleep(4)
    py.click(1126,101) # export the har file
    time.sleep(1)
    py.click(159,405) #click the folder where you want to store all the data (in this it is website_data)
    py.sleep(2)
    py.click(1318,56) #press save button
    time.sleep(4)
    py.click(706,107) #clear the logs


url_list = getwebList(filename) #store the list of websites into a list

url_list = cross_check_list(url_list) #if a website has already been logged and the har file is in the folder, it will remove that website from the list

run_automation(url_list)
