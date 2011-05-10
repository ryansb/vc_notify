#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks Github and Bitbucket and notifies if there are new commits
# Version 1.0.0
import pynotify
import feedparser
from BeautifulSoup import BeautifulSoup
import time
import re

if not pynotify.init("Version Control Notifier"):
	exit()

displayed_messages = []
count = 0

def pull_feeds():
	#Returns a list of raw version control feeds
	key_arr = re.split('\s', open('keys.txt').read())
	feeds = []
	for key in key_arr:
		feeds.append(feedparser.parse(key))
	return feeds

while(1):
	for i in pull_feeds():
		for j in i['entries']:
			soup = BeautifulSoup(j['summary'])
			if(soup.find('p')):
				n = pynotify.Notification(j['title'], soup.find('p').text)
			if(soup.find('blockquote')):
				n = pynotify.Notification(j['title'], soup.find('blockquote').text)
			if(not displayed_messages.__contains__(j['id'])):
				n.show()
				displayed_messages.append(j['id'])
			count += 1
			if count > 4:
				break
	time.sleep(30)

#n = pynotify.Notification("Title", "Message")
#n.show()
