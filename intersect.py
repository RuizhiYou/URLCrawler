import json
import matplotlib.pyplot as plt
import domain_utils as du
files = ['calvin_internal_links.json','thomas_internal_links.json','rui_internal_links.json', 'louis_internal_links.json']
jsondata = []
for f in files:
    jsonfile = open(f)
    jsonstr = jsonfile.read()
    jsondata.append(json.loads(jsonstr))

finaltld = {}

def parse(string):
  return string.split("/")[2]
  #for other understanding of TLD+1, use the below return function
  #return "".join([str.split("/")[2], "/", str.split("/")[3]])

results = [set() for i in range(4)]
frequencey_dict = {}
for k in range(len(jsondata)):
    for i in range(len(jsondata[k])):
        for j in jsondata[k][i][1]:
            if j.startswith("http"):
                tld = du.get_ps_plus_1(j)
                results[k].add(tld)

intersect = (results[0].intersection(results[1])).intersection(results[2]).intersection(results[3])
f = open('intersect.json', 'w')
print(len(intersect))
json.dump(list(intersect), f)
f.close()

