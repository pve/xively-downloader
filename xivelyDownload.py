# coding=utf-8
import requests
from config import *
import datetime
import time

out = open('./outPut.csv', 'a')

cache = ""
endstring = "" 
while (time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) < time.mktime(datetime.datetime.strptime(stop, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())):
	endstring = str(datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) + 5*3600).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
	url = 'https://api.xively.com/v2/feeds/' + feedID + '.csv?start=' + start + '&end=' + endstring + '&limit=1000&interval=0'
	print url
	cache = endstring # if we get zero results, we want to move to the next window.
	page = requests.get(url, auth=(login, pwd))
	if page.status_code != 200 :
		print page.status_code 
	page.raise_for_status()
# xively returns the boundary values twice
	lines = page.content.split('\n')
	print "#lines" , len(lines)
	for line in lines:
		splitline = line.split(',')
		if len(splitline)!= 3 :
			print  len(splitline) , line
		else: 
			out.write(splitline[0]+ ',' + 
			datetime.datetime.strptime(splitline[1], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S") + 
			',' + splitline[2] + '\n')
#			out.write(line + '\n')
			cache = line.split(',')[1]
		
#	start = cache.split('.')[0] + 'Z'
	start = cache
#	make sure we dont ask the same question twice
	start = str(datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) + 1).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
out.close()
