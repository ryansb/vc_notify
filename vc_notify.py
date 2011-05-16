#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks Github and Bitbucket and notifies if there are new commits
# Usage: Put the Atom or RSS feeds for your version control solution (currently
# only supports Github and BitBucket) in a file named keys.txt separated by
# whitespace (tabs, spaces, or newlines) and run vc_notify.py
# Version 1.0.0
from pynotify import Notification
from pynotify import init
from feedparser import parse
from BeautifulSoup import BeautifulSoup
from time import sleep
from re import split
from sys import argv
import os

if not init("Version Control Notifier"):
	exit()

displayed_messages = []
count = 0


def pull_feeds():
	key_arr = []
	#Returns a list of raw version control feeds
	if len(argv) == 2:
		try:
			key_arr = split('\s', open(argv[1]).read())
		except Exception:
			print ("Couldn't open keys file, bad argument passed"
				+ "in")
	else:
		try:
			keys_path = os.path.abspath(__file__)
			key_arr = split('\s', open(keys_path.replace('vc_notify.py', 'keys.txt')).read())
		except Exception:
			print ("Couldn't find the keys file, make sure it's in"
			+ "the same directory as the script")
	feeds = []
	for key in key_arr:
		feeds.append(parse(key))
	return feeds

while(1):
	for i in pull_feeds():
		for j in i['entries']:
			soup = BeautifulSoup(j['summary'])
			if(soup.find('p')):
				n = Notification(j['title'],
						soup.find('p').text)
			if(soup.find('blockquote')):
				n = Notification(j['title'],
						soup.find('blockquote').text)
			if(not displayed_messages.__contains__(j['id'])):
				displayed_messages.append(j['id'])
				if n:
					n.show()
			count += 1
			if count > 4:
				break
	sleep(30)

#n = pynotify.Notification("Title", "Message")
#n.show()
