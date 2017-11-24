import json
import csv

fin = open("intersect.json", 'r')
fout = open("intersect.csv", 'w', newline='')

fieldnames = ['url']
writer = csv.DictWriter(fout, fieldnames=fieldnames)

writer.writeheader()
data = json.loads(fin.read())
fin.close()
for e in data:
    writer.writerow({'url':e})

fout.close()
