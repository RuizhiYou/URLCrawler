import json
import matplotlib.pyplot as plt
import urlparse
import domain_utils as du
files = ['union.json','intersect.json']
jsondata = []
for f in files:
    jsonfile = open(f)
    jsonstr = jsonfile.read()
    load = json.loads(jsonstr)
    jsondata.append(load)

print("====>Size of union set")
print len(jsondata[0])
print("====>Size of intersection set")
print len(jsondata[1])

f = open("difference.txt","w")
difference = set(jsondata[0]).intersection(set(jsondata[1]))
f.write(str(difference))
f.close()

