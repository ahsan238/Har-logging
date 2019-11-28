import os
import re
import time
import sys
from os import listdir
from os.path import isfile, join

import pyautogui as py

wait_time = int(sys.argv[1])
scorlling = True


# grab the sites to visit (rank, domain) format
filename = 'top-1m.csv'


def getwebList(filename):
  sites = []
  for l in open(filename).readlines():
    site = l.strip().split(",")
    #print (site)
    if len(site)<2:
      print ("Problem with input file format!", site)
    sites.append(site[1])
  #print (len(sites))
  return sites

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
  for url in url_list[:4]:
    print ('crawling: ',url)
    # py.click(706,107) #clear the log
    py.click(527, 70) #click url bar
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite(str(url)) #enter url
    py.press("enter") #press enter
    time.sleep(wait_time) #wait for the website to load
    if scorlling == True: #perform scrolling if enabled
      py.moveTo(384,312)
      py.scroll(-30) #takes as argument number of pixels to scroll
      time.sleep(4)
    py.click(1230,100) # export the har file
    time.sleep(1)
    py.click(260,365) #click the folder where you want to store all the data (in this it is website_data)
    py.sleep(2)
    py.click(690,50) #press save button
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite(str(url)+'.har') #enter url
    time.sleep(1)
    py.click(1320,45) #press save button
    time.sleep(4)
    py.click(806,95) #clear the logs
    time.sleep(2)


url_list = getwebList(filename) #store the list of websites into a list
#print (len(url_list))
url_list = cross_check_list(url_list) #if a website has already been logged and the har file is in the folder, it will remove that website from the list
#print (len(url_list))
run_automation(url_list)
