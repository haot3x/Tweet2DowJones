#! /usr/bin/python

import json
from datetime import datetime

def convert_datetime(timestamp):
	return datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')

def date_handler(obj):
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj


INPUT = 'dji_raw.json'
OUTPUT = 'dji_1hr.json'

time_interval = convert_datetime("2014-04-07 11:00:00") - convert_datetime("2014-04-07 10:00:00")
#print time_interval

objs = json.load(open(INPUT, 'r'))
#print len(objs)


current_datetime = convert_datetime(objs[0]['timestamp'])
#current_datetime = objs[0]['timestamp']
count = 0
total = 0.0


result = []

for o in objs:
	tmp_datetime = convert_datetime(o['timestamp'])
	#tmp_datetime = o['timestamp']
	tdelta = tmp_datetime - current_datetime
	if (tdelta < time_interval):
		count = count + 1
		total = total + float(o['dji'])
	else:
		#element = {'timestamp': current_datetime, 'dji': total/count}
		result.append([current_datetime.strftime("%Y-%m-%d %H:%M:%S"), total/count])

		current_datetime = tmp_datetime
		total = float(o['dji'])
		count = 1

di = {'name': 'DJI', 'series': result}

f = open(OUTPUT, 'w+')
f.write(json.dumps(di, default=date_handler))
f.close()
