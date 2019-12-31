import os
import re
import json
import socket
from urllib.parse import urlsplit

# custom webxray classes
# from webxray.ParseURL import ParseURL

# # browsers
# from webxray.ChromeDriver import ChromeDriver

class ParseURL:

  def __init__(self):
    # load up the tld list now as only hit it once this way
    self.pubsuffix_list = self.get_pubsuffix_list()
  # end __init__

  def get_pubsuffix_list(self):
    """
      this builds a shared list of tuples based on the pubsuffix list; tuples allow for
      quick comparisons of smaller strings
    """

    # path is relative from root webxray directory
    pubsuffix_raw_list = open('public_suffix_list.dat', mode='r', encoding='utf8')
    pubsuffix_list = []

    for line in pubsuffix_raw_list:
        # the last part of the list is random stuff we don't care about, so stop reading
        if re.match("^// ===BEGIN PRIVATE DOMAINS===", line):break

        # skip lines that are comments or blank, add others to list
        if not re.match("^//.+$|^$", line):
          # remove leading ., !, and * as it screws up regex later
          pubsuffix_string = re.sub('^[\!\*]\.?', '', line.strip())

          # convert to idna/ascii/utf-8 for enhanced compatability
          pubsuffix_string = pubsuffix_string.encode('idna').decode('utf-8')

          # convert to a tuple so we can do faster comparisons
          pubsuffix_list.append(tuple(pubsuffix_string.split('.')))

    # add the pubsuffix for tor addresses
    pubsuffix_list.append(('onion',))

    # done
    return pubsuffix_list
  # get_pubsuffix_list

  def get_ip_fqdn_domain_pubsuffix_tld(self,url):
    """
      Given a url string, this class will return the ip address, fully-qualified domain name,
        domain, public suffix, and top-level domain as a tuple.
    """

    # first make sure it is actually an https? or wss? request we can parse
    # if not (re.match('^(https?|wss?)://.+', url)):
    #   # print ("got rejected here")
    #   return None

    try:
       # try to pull out the fully-qualified domain name (fqdn) from the netloc
      # with some regex, handles cases where the port is included (eg 'example.com:1234')
      # drops leading/trailing '.', etc.
      fqdn = re.search('^(\.+)?(.+?)(:.+)?(\.+)?$', urlsplit(url).netloc).group(2)

      # convert to idna/ascii/utf-8 for enhanced compatability
      fqdn = fqdn.encode('idna').decode('utf-8')
    except:
      print ("rejection with url",url)
      return None

    # to see if the fqdn is simply an ip_addr try to load it as such
    # return the IP for all fields even though not strictly
    # accurate as to field values
    try:
      ip_addr = socket.inet_aton(fqdn)
      return(fqdn, fqdn, fqdn, None, None)
    except socket.error:
      pass

    # if the fqdn is not an ip_addr we use socket to get the ip_addr
    try:
      ip_addr = socket.gethostbyname(fqdn)
    except:
      ip_addr = None

    # convert what we have to a tuple and match against our list
    domain_tuple = tuple(fqdn.split('.'))
    num_tokens = len(domain_tuple)
    slice_point = 0

    # we keep dropping off the left-most token until we find a match
    # this way we match on "ac.uk" *before* "uk"
    while slice_point < num_tokens-1:
      slice_point += 1
      pubsuffix = domain_tuple[slice_point:]
      if pubsuffix in self.pubsuffix_list:
        # we found the pubsuffix, 1 back is the domain
        domain = domain_tuple[slice_point-1:]
        # tld is always the final token
        tld = domain_tuple[num_tokens-1]
        # found match, return as single strings joined on '.'
        return (ip_addr, fqdn, '.'.join(domain), '.'.join(pubsuffix), tld)

    # if we get to this point nothing else has worked
    return None
  # get_domain_pubsuffix_tld
#end ParseURL



domain_owners  = {}
id_to_owner  = {}
id_to_parent = {}

# set up the domain ownership dictionary
for item in json.load(open('domain_owners.json', 'r', encoding='utf-8')):
  id_to_owner[item['id']]  = item['owner_name']
  id_to_parent[item['id']]   = item['parent_id']
  for domain in item['domains']:
    domain_owners[domain] = item['id']
# end init
# print (id_to_owner)

def get_lineage(id):
  if id_to_parent[id] == None:
    return [id]
  else:
    return [id] + get_lineage(id_to_parent[id])



# filename = "total_trackers_LTE.json"
filename = "total_trackers_LTE.json"

def check_tracker_domain(filename):
  url_domain_company_mapping = {} #for each url that we visit, we process all the domains which were seriving the visited url with objects (js, img etc) and we map these domains to their parent companies
  url_parser = ParseURL()
  data = {}
  with open(filename) as file:
    data = json.load(file)
    file.close()
  url_count = 0

  for url in data:
    url_count+=1
    element_domains = []
    print ('\n\n',str(url_count),'/',str(len(data.keys())),'.........................',url)
    origin_ip_fqdn_domain_pubsuffix_tld = url_parser.get_ip_fqdn_domain_pubsuffix_tld("https://"+url)
    if origin_ip_fqdn_domain_pubsuffix_tld is None:
      print('could not parse origin domain', url)
      continue

    # if we can't get page domain info we bail out

    origin_ip       = origin_ip_fqdn_domain_pubsuffix_tld[0]
    origin_fqdn     = origin_ip_fqdn_domain_pubsuffix_tld[1]
    origin_domain     = origin_ip_fqdn_domain_pubsuffix_tld[2]
    origin_pubsuffix  = origin_ip_fqdn_domain_pubsuffix_tld[3]
    origin_tld      = origin_ip_fqdn_domain_pubsuffix_tld[4]

    for request in data[url]["third_party"]: #NOTEEEE --> CHECK THIS (data[url]["third_party"]?)
      # print(request)
      url_tracker_domains_info = []
      element_ip_fqdn_domain_pubsuffix_tld = url_parser.get_ip_fqdn_domain_pubsuffix_tld(request)
      if element_ip_fqdn_domain_pubsuffix_tld is None:
        continue
      element_ip      = element_ip_fqdn_domain_pubsuffix_tld[0]
      element_fqdn    = element_ip_fqdn_domain_pubsuffix_tld[1]
      element_domain    = element_ip_fqdn_domain_pubsuffix_tld[2]
      element_pubsuffix   = element_ip_fqdn_domain_pubsuffix_tld[3]
      element_tld     = element_ip_fqdn_domain_pubsuffix_tld[4]

      if origin_domain not in element_domain:
        if element_domain not in element_domains:
          element_domains.append(element_domain)
      element_domains.sort()

      count = 0
      for domain in element_domains:
        count += 1

        if domain in domain_owners:
          lineage = ''
          for item in get_lineage(domain_owners[domain]):
            lineage += id_to_owner[item]+' > '
          # print('\t%s) %s [%s]' % (count, domain, lineage[:-3]))
          url_tracker_domains_info.append('%s [%s]' % (domain, lineage[:-3]))
          # url_tracker_domains_info = list(set(url_tracker_domains_info))
          # print(url_tracker_domains_info)
        else:
          # print('\t%s) %s [Unknown Owner]' % (count, domain))
          url_tracker_domains_info.append('%s [Unknown Owner]' % (domain))

    url_tracker_domains_info = list(set(url_tracker_domains_info))

    url_domain_company_mapping[url] = url_tracker_domains_info
    # print(url_tracker_domains_info)
  outputFile = "LTE_domains.json"
  with open(outputFile, 'w') as fp:
    json.dump(url_domain_company_mapping , fp,indent = 4)
    fp.close()


check_tracker_domain(filename)
