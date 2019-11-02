# Useful Script for my Sproj on mobile tracking

## browser_auto.py

### the browser_auto script is the autologging script. It contains a set of instructions that automate clicks and keyboard hits. But for the script to work on a particular host machine, precise positions of pixels need to added to the script.

```def run_automation(url_list):
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
    ```
