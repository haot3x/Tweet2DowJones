#!/usr/bin/python

import json
from random import randint

INPUT = "dji_15mins.json"
OUTPUT = 'dji_15mins_perc.json'

def date_handler(obj):
    import datetime
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj

obj = json.load(open(INPUT,'r'))

print len(obj['series'])

perc = [0]
for i in xrange(1,len(obj['series'])):
    prev = obj['series'][i-1][1]
    cur = obj['series'][i][1]
    p = (cur-prev)/prev
    perc.append(p)

max_perc = max([abs(x) for x in perc])
se = map(lambda x : [x[0][0],x[1]/max_perc] ,zip(obj['series'],perc))
di = {'name':'DJI perc','series':se}

print len(di['series'])

f = open(OUTPUT,'w+')
f.write(json.dumps(di,default=date_handler))
f.close()
