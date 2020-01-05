import json
import os
import pickle

def get_cookies(fileName):
  cookieList = []
  with open (fileName) as file:
    parsed_json = json.load(file)
    for i in range(len(parsed_json["log"]["entries"])):
      entry = parsed_json["log"]["entries"][i]["response"]["cookies"]
      if not entry:
        continue
      cookieList.append(entry)
  file.close()
  return cookieList

def save_list_to_file(listName, outputFilename):
  with open(outputFilename,'w') as f:
    for s in listName:
      f.write(str(s)+'\n\n')
  f.close()

cookie_list = get_cookies("./m.twitch.tv.har")
save_list_to_file(cookie_list,"cookieList.txt")
