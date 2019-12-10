import json
import os

# count = 0
# os.system(("pagexray --pretty ./har\ 3g/{} > ./har\ 3g/json\ files/{}").format(entry,json_file_name))

def create_json_from_har(dir):
  entries = os.listdir(dir)
  connection_type = 'LTE' if 'LTE' in dir else 'wifi'
  for entry in entries:
    if '.har' in entry:
      # count += 1
      # json_file_name = str(entry).replace('.har','_{}.json'.format(connection_type))
      json_file_name = str(entry).replace('.har','.json')
      print (json_file_name)
      # dir_name = '3g' in dir? './har\ 3g/':'./har\ wifi/'
      dir_name = './../tracking_data/Samsung\ s9\ LTE/' if 'LTE' in dir else './../tracking_data/nexus\ 5\ WIFI/'
      # print((("pagexray --pretty {}{} > {}json_files/{}").format(dir_name,entry,dir_name,json_file_name)))
      # print ("{}{}".format(dir_name,entry))
      # print (("pagexray --pretty {}{} > {}json/{}").format(dir_name,entry,dir_name,json_file_name))
      os.system(("pagexray --pretty --includeAssets {}{} > {}json/{}").format(dir_name,entry,dir_name,json_file_name))
      # break
      # breaks


def remove_brackets_from_json(dir):
  entries = os.listdir(dir)
  # print entries
  for entry in entries:
    with open(dir+'/'+entry) as file:
      file.seek(0,os.SEEK_END)
      print (file.readline())
      file.close()




# dir = './../data/nexus 5 WIFI'
# remove_brackets_from_json(dir)
# create_json_from_har('./../tracking_data/Samsung s9 LTE')
create_json_from_har('./../tracking_data/nexus 5 WIFI')

# print (count)

# dic = {"wifi":{"domain":{"www.google.com":}}}
