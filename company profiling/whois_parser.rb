require 'rubygems'
require 'whois'
require 'whois-parser'


def transform_file(filename) #this is a bogus function, i used to practice syntax for ruby since im new the language.
  file = File.open(filename)
  file_data = file.readlines.map(&:chomp)
  for i in 0..file_data.size-1 do
    if file_data[i]["12"] == nil
      file_data[i] = file_data[i].sub('a','12')
    end
  end
  file.close
  # open a new file and copy the transformed contents to it
  File.open("1234","w+") do |f|
    f.write file_data.join("\n")
  end
  puts file_data
end

# transform_file("123")
def get_whois_admin_list(domain) #returns the list of admins responsible for the domain passed into the function
  begin
      whois = Whois.whois(domain)
      parser = whois.parser
      admin_list = parser.admin_contacts
      organization_name = ""
      for i in 0..admin_list.size-1 do
        organization_name = organization_name+admin_list[i].organization
      end
      return organization_name
    raise "Error occured while processing domain: #{domain}"
  rescue
    return nil
  end
end



def push_whois_response(filename) # this function visits each line in the file which was created when we ran the python file "scan_trackers_domains.py". If a domain has not been associated with any admin, this functions tries to find the admin through whois. If it gets a valid response then it will modify that line otherwise it will leave the line as it is.
  type_network = "LTE"
  file = File.open(filename)
  file_data = file.readlines.map(&:chomp)
  for i in 0..file_data.size-1 do #visit each line to check for Unknown keyword
    domain = file_data[i].split(' ')[0] #get the domain from the line
    puts "#{domain} => #{i}"
    if file_data[i]["Unknown"] != nil
      admin = get_whois_admin_list(domain)
      if admin != nil
        file_data[i] = file_data[i].sub("Unknown",admin)
      end
    end
  end
  puts file_data
  file.close
  File.open("whois_modified_#{type_network}","w+") do |f|
    f.write file_data.join("\n")
  end
end

push_whois_response("LTE_only_domains")

# def push_ws(filename) # this function visits each line in the file which was created when we ran the python file "scan_trackers_domains.py". If a domain has not been associated with any admin, this functions tries to find the admin through whois. If it gets a valid response then it will modify that line otherwise it will leave the line as it is.
#   type_network = "LTE"
#   file = File.open(filename)
#   file_data = file.readlines.map(&:chomp)
#   for i in 0..file_data.size-1 do #visit each line to check for Unknown keyword
#     domain = file_data[i].split(' ')[0] #get the domain from the line
#     puts "#{domain}"
#   end
# end
