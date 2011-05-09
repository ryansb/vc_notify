#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks Github and Bitbucket and notifies if there are new commits
# Version 1.0.0
import pynotify
import feedparser
from BeautifulSoup import BeautifulSoup
import time

if not pynotify.init("Version Control Notifier"):
	exit()

displayed_messages = []
count = 0

def pull_feeds():
	#Returns a list of raw version control feeds
	#Bitbucket feed (0)
	feed =feedparser.parse("https://bitbucket.org/rbrown/atom/feed?token=0ab0af15b07352b1596a30bed1293615")
	#Github feeds (1)
	feed2 =feedparser.parse("https://github.com/ryansb.private.actor.atom?token=cae0b3520b731518fcc0f2fc683cae31")
	return [feed, feed2]

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
