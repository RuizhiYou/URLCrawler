import json
import matplotlib.pyplot as plt
import urlparse
import domain_utils as du

jsonfile = open('thomas_internal_links.json')
jsonstr = jsonfile.read()
jsondata = json.loads(jsonstr)

finaltld = {}

def parse(string):
  return string.split("/")[2]
  #for other understanding of TLD+1, use the below return function
  #return "".join([str.split("/")[2], "/", str.split("/")[3]])
result = {}
frequencey_dict = {}
for i in range(len(jsondata)):
  for j in jsondata[i][1]:
    if j.startswith("http"):
        tld = du.get_ps_plus_1(j)
        if tld in result:
            result[tld] += 1
        else:
            result[tld] = 1
for key in result:
        if result[key] in frequencey_dict:
            frequencey_dict[result[key]] += 1
        else:
            frequencey_dict[result[key]] = 1
print (result)
print len(result)
