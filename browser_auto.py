import os
import re
import time
import sys
from os import listdir
from os.path import isfile, join
import pyautogui as py
from subprocess import Popen, PIPE
import subprocess
import traceback


""" global variables"""
scorlling = True
# grab the sites to visit (rank, domain) format
filename = 'top-1m.csv'
dirname = 'site_LTE_4'
CHROME = "com.android.chrome"
ACTIVITY = "/com.google.android.apps.chrome.Main"
END = 1000
START = 0

def create_dir(db_path):
    """ create a dir """
    try:
        if not os.path.isdir(db_path):
            os.mkdir(db_path)
            print ('Database dir created')
        else:
            print ('Database dir already exists. Will append to existing database')
    except Exception as e:
        print (e)
        return 0
    return 1

def getwebList(filename):
  sites = []
  for l in open(filename).readlines():
    site = l.strip().split(",")
    #print (site)
    if len(site)<2:
      print ("Problem with input file format!", site)
    sites.append(site[1])
  #print (len(sites))
  return sites[START:END]

def cross_check_list(url_list):
  # entries = os.listdir('./..')
  mypath = dirname+'/old'
  entries = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  new_list = []
  print (len(set(url_list)))
  print (len(set(entries)))
  count = 0
  for f in entries:
    #if os.path.getsize(join(mypath,f))<10*1024:
    #  count += 1
    #  continue
    if f[:-4] in url_list: #removing '.har'
      url_list.remove(f[:-4])
  print (count)
  return url_list


def run_automation(url_list):

  for url in url_list:

    ## clear all storage for browser
    r = subprocess.Popen("adb shell pm clear "+ CHROME, shell=True)
    r.wait()
    time.sleep(3)


    ## open browser and try to load blank page first
    r = subprocess.Popen("adb shell am start -n "+ CHROME + ACTIVITY + " -a android.intent.action.VIEW -d about:blank --es 'com.android.browser.application_id' "+ CHROME, shell=True)
    r.wait()
    time.sleep(3)

    ## wait for browser to start
    found = 0
    while True:
        r = subprocess.Popen(" adb shell ps | awk '{print $9}'", shell =True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = r.communicate()
        for l in out.splitlines():
            if CHROME in l.decode():
                found = 1
                break
        if found:
            break   
        else:
            r = subprocess.Popen("adb shell am start -n "+ CHROME + ACTIVITY + " -a android.intent.action.VIEW -d about:blank --es 'com.android.browser.application_id' "+ CHROME, shell=True)
            r.wait()


    ## prepare the browser
    '''
        This specific taps are relevant to chrome to bypass intial settings
    '''
    # click not sharing checkbox
    r = subprocess.Popen("adb shell input tap 100 1200", shell=True)
    r.wait()
    time.sleep(1)
    # click the start browsing
    r = subprocess.Popen("adb shell input tap 500 1700", shell=True)
    r.wait()
    time.sleep(3)
    # click the no sync
    r = subprocess.Popen("adb shell input tap 150 1700", shell=True)
    r.wait()
    time.sleep(1)

    # click the text box
    r = subprocess.Popen("adb shell input tap 450 675", shell=True)
    r.wait()
    time.sleep(2)


    py.click(1249,734) # press inspect button

  
    print ('crawling: ',url)

    '''
    # py.click(706,107) #clear the log
    py.click(484, 125) #click url bar
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite(str(url)) #enter url
    py.press("enter") #press enter
    '''
    
    ## have to enter specific website URL text
    # click the text bar
    r = subprocess.Popen("adb shell input tap 400 140", shell=True)
    r.wait()
    time.sleep(1)

    r = subprocess.Popen("adb shell input text "+"http://"+url, shell=True)
    r.wait()
    time.sleep(1)

    r = subprocess.Popen("adb shell input keyevent 66", shell=True) #press enter
    r.wait()
    time.sleep(wait_time) #wait for the website to load

    if scorlling == True: #perform scrolling if enabled
      py.moveTo(536, 208)
      py.scroll(-30) #takes as argument number of pixels to scroll
      time.sleep(5)
    py.click(1230,156) # export the har file
    time.sleep(1)
    py.click(256,326) #click the folder where you want to store all the data (in this it is website_data)
    py.sleep(2)
    py.click(637,46) #press filename bar
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite(str(url)+'.har') #enter url
    time.sleep(1)
    py.click(1325,50) #press save button
    time.sleep(5)
    py.click(1284,103) #press save button
    time.sleep(1)
    '''
    py.click(527, 70) #click url bar
    py.hotkey("ctrlleft","a","backspace") #clear the tab
    py.typewrite('about:blank') #enter blan page to stop any further loads
    py.press("enter") #press enter
    time.sleep(2)
    py.click(804,156) #clear the logs
    time.sleep(2)
    '''


""" main function """
if len(sys.argv)<2:
  print ('Wrong format: python3 .py waititme')
  exit(1)

wait_time = int(sys.argv[1])

create_dir(dirname)

url_list = getwebList(filename) #store the list of websites into a list
#print (len(url_list))
url_list = cross_check_list(url_list) #if a website has already been logged and the har file is in the folder, it will remove that website from the list
print (len(url_list))
run_automation(url_list)
