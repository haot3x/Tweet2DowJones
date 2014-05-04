#! /usr/bin/python
import json
from datetime import datetime

def convert_datetime(timestamp):
	return datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')

def date_handler(obj):
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj


INPUT = 'emotioni+dont+feel2777.json'
OUTPUT = 'emotioni+dont+feel2777.json_output.json'


def generate_emotion():
	