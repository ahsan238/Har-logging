from adblockparser import AdblockRules
import json
import os
import tldextract
import pprint
filename = 'easy_list.txt'
pp = pprint.PrettyPrinter(indent=2)


def mime_type_to_easylist_type(mime_type):

  switcher = {
   "html": "document",
   "application/x-javascript": "script",
   "javascript": "script",
   "css": "stylesheet",
   "image/svg+xml": "image",
   "image/webp": "image",
   "image": "image",
   "image/gif": "image",
   "image/x-icon": "image",
   "image/jpeg": "image",
   "application/font-woff2": "font",
   "font-woff2": "font",
   "video/mp4": "media",
   "favicon":" image",
   "other": "other",
   "plain": "other",
   "json": "other"
  }
  return switcher.get(mime_type, "other")



def load_rules (filename):
  lineList = []
  with open (filename) as f:
    lineList = f.readlines()
  return lineList

def load_scripts_from_json(filename):
  requested_files = []
  # parsed_json = (json.loads(filename))
  with open (filename) as f:
    parsed_json = json.load(f)
    parsed_json = parsed_json[0]
    f.close()
  for i in parsed_json["assets"]:
    requested_files.append(i)
  return requested_files
  # print parsed_json["assets"][0]["url"]

def find_tracker_urls(dir): #finds third party tracker urls
  entries = os.listdir(dir)
  wifi_dict = {}
  count = 0
  print 1
  for entry in entries:
    # count+=1
    # if count == 10:
    #   break
    requested_files = load_scripts_from_json(dir+entry)
    entry = entry.replace(".json","")
    print entry
    wifi_dict[entry] = {}
    # print wifi_dict
    wifi_dict[entry]["first_party"] = []
    wifi_dict[entry]["third_party"] = []
    webpage_domain = tldextract.extract(entry).domain
    for i in requested_files:
      url_request_domain = tldextract.extract(i["url"]).domain
      requested_file_type = mime_type_to_easylist_type(i["type"])
      if webpage_domain in url_request_domain:
        options = {'third_party':'False',requested_file_type:'True'}
        if rules.should_block(i["url"],options) == True:
          wifi_dict[entry]["first_party"].append(i["url"])
      else:
        options = {'third_party':'True',requested_file_type:'True'}
        if rules.should_block(i["url"],options) == True:
          wifi_dict[entry]["third_party"].append(i["url"])

  # print pp.pprint(wifi_dict)
  return wifi_dict


def get_numbers(url_dict):
  num_dict = {}
  for url in url_dict:
    num_dict[url] = {}
    num_dict[url]["first_party"] = len(url_dict[url]["first_party"])
    num_dict[url]["third_party"] = len(url_dict[url]["third_party"])
  return num_dict


raw_rules = load_rules(filename)
filename = "easy_privacy.txt"

#combine the two rules
raw_rules_two = load_rules(filename)
combined_rules = raw_rules+raw_rules_two
rules = AdblockRules(combined_rules)

# rules = AdblockRules(raw_rules)

# print mime_type_to_easylist_type("image")



dir = "./../tracking_data/nexus 5 WIFI/json/"
total_trackers = find_tracker_urls(dir) #stores complete information about all detected trackers
tracker_numbers = get_numbers(total_trackers) #stores the number of trackers detected per website
# print pp.pprint(num_dict)
if 'WIFI' in dir:
  output_total_file_name = "total_trackers_WIFI.json"
  output_number_file_name = "number_trackers_WIFI.json"
else:
  output_total_file_name = "total_trackers_LTE.json"
  output_number_file_name = "number_trackers_LTE.json"
  # 'WIFI' in dir? "number_trackers_WIFI.json": "total_trackers_LTE.json"
  # "total_trackers_WIFI.json": "total_trackers_LTE.json"


with open(output_total_file_name, 'w') as fp:
  json.dump(total_trackers , fp,indent = 4)
  fp.close()
with open(output_number_file_name, 'w') as fp:
  json.dump(tracker_numbers, fp,indent = 4)
  fp.close()
# f = open('dict.txt','w')
# f.write(str(wifi_dict))
# f.close()


