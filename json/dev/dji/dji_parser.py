#! /usr/bin/python

import json
from datetime import datetime

def convert_datetime(timestamp):
	return datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')

def date_handler(obj):
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj


DJI_INPUT = 'dji_raw.json'
DJI_OUTPUT = 'dji_15mins.json'

EMOTION_INPUTS = {'../emotion/emotioni+dont+feel2777.json'}


time_interval = convert_datetime("2014-04-07 11:00:00") - convert_datetime("2014-04-07 10:45:00")
#print time_interval

emotiondict = list()

def generate_dji():
	objs = json.load(open(DJI_INPUT, 'r'))
	#print len(objs)
	current_datetime = convert_datetime('2014-04-07 11:00:00')
	#current_datetime = objs[0]['timestamp']
	count = 0
	total = 0.0
	result = []
	result_contain_weekend = list()

	for o in objs:
		tmp_datetime = convert_datetime(o['timestamp'])
		#tmp_datetime = o['timestamp']
		#tdelta = tmp_datetime - current_datetime
		if (tmp_datetime - current_datetime < time_interval):
			count = count + 1
			total = total + float(o['dji'])
		else:
			element = {'timestamp': current_datetime, 'value': total/count}
			result_contain_weekend.append(element)
			#result.append([current_datetime.strftime("%Y-%m-%d %H:%M:%S"), total/count])

			# build time table to count emotion tweets
			#element = {'timestamp': current_datetime, 'pos': 0, 'neg': 0}
			#emotiondict.append(element)

			current_datetime += time_interval
			total = float(o['dji'])
			count = 1


	for elem in result_contain_weekend:
		if elem['timestamp'].isoweekday() < 6:
			#build emotion dict
			element = {'timestamp': elem['timestamp'], 'pos': 0, 'neg': 0}
			emotiondict.append(element)

			#write dji data
			result.append([elem['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), elem['value']])

	di = {'name': 'DJI', 'series': result}

	#f = open(DJI_OUTPUT, 'w+')
	#f.write(json.dumps(di, default=date_handler))
	#f.close()






def insert_to_emotiondict(created_time, emotion):
	size = len(emotiondict)
	if (created_time > emotiondict[size-1]['timestamp']):
		return
	if (created_time < emotiondict[0]['timestamp']):
		emotiondict[0][emotion] += 1
		#print emotiondict[0]
		return

	for i in range(1, size):
		if (created_time > emotiondict[i-1]['timestamp'] and created_time <= emotiondict[i]['timestamp']):
			emotiondict[i][emotion] += 1
			#print emotiondict[i]
			return
	return


def generate_emotion():
	for emotion_input in EMOTION_INPUTS:
		objs = json.load(open(emotion_input, 'r'))

		result = []
		for o in objs:
			created_time = convert_datetime(o['created_at'])
			emotion = o['classification']
			#print created_time, emotion
			insert_to_emotiondict(created_time, emotion)
			#raw_input()

		# for elem in emotiondict:
		# 	print elem
		for elem in emotiondict:
			result.append([elem['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), float(elem['pos'])/float(elem['pos']+elem['neg']+1)])

		name = emotion_input[18:len(emotion_input)-5]
		outfile = emotion_input[:len(emotion_input)-5]+'_parsed.json'
		print name
		print outfile

		di = {'name': name, 'series': result}


		f = open(outfile, 'w+')
		f.write(json.dumps(di, default=date_handler))
		f.close()


def test():
	size = 10
	for i in range(0, size):
		print i


generate_dji()
generate_emotion()


