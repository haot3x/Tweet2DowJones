#!/usr/bin/python

import json
from random import randint

INPUT = "Tweet.size1000page1cnt849.json"
OUTPUT = 'new.json'


objs = json.load(open(INPUT,'r'))
print len(objs)

# for k,v in objs[0].items():
#     print "%s=\n\t%s | " % (str(k),str(v))

def date_handler(obj):
    import datetime
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj

se = []
for o in objs:
    # se.append( {'x':o['created_at'],'y':randint(0,1000)} )
    se.append([o['created_at'],randint(0,1000)])

di = {'name':'LA','series':se}
# print json.dumps(di)
# print type(di['series'][0][0])

f = open(OUTPUT,'w+')
f.write(json.dumps(di,default=date_handler))
f.close()
