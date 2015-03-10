import json
import os
import sys
from pprint import pprint

LEAPYEARS = ['2012','2008','2004','1996','1992']

path,datafile = os.path.split(sys.argv[1])

with open(os.path.join(path,datafile),'r') as infile:
    data = json.load(infile)

with open(os.path.join(path,'no_229_'+datafile),'w') as savefile:
    json.dump(data,savefile)

for year in LEAPYEARS[:1]:  
    del data[year][59]
    for dayda in data[year][59:]:
        dayda['day'] -= 1

with open(os.path.join(path,datafile),'w') as outfile:
    json.dump(data,outfile)
