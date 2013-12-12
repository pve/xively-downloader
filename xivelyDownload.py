# coding=utf-8
import requests
from config import *
import datetime
import time

out = open('./outPut.csv', 'a')

cache = ""
while (time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) < time.mktime(datetime.datetime.strptime(stop, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())):
	url = 'https://api.xively.com/v2/feeds/' + feedID + '.csv?start=' + start + '&end=' + str(datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) + 6*3600).strftime('%Y-%m-%dT%H:%M:%S.%fZ')) + '&limit=1000&interval=0'
	page = requests.get(url, auth=(login, pwd))
# xively returns the boundary values twice
	lines = page.content.split('\n')
	for line in lines:
#		out.write(line.split(',')[1] + ',' + line.split(',')[2] + '\n')
		out.write(line + '\n')
		cache = line.split(',')[1]
		
#	start = cache.split('.')[0] + 'Z'
	start = cache

out.close()
