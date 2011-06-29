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

class Notifier():
	def __init__(cls):
		cls.count = 0
		cls.displayed_messages = []
		cls.initial_pull()
		while(1):
			cls.parse_all()
			sleep(30)

	def initial_pull(cls):
		n = Notification("Version Control Notifier started", "Version Control Notifier will now notify you of any changes via libnotify")
		n.show()
		feeds = cls.pull_feeds()
		cls.parse_bitbucket(feeds[0], display=False)
		cls.parse_github(feeds[1], display=False)
		cls.parse_chili(feeds[2], display=False)

		return True

	def pull_feeds(cls):
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
				key_arr = split('\s', open(keys_path.replace('vc_notify.py',
					'keys.txt')).read())
			except Exception:
				print ("Couldn't find the keys file, make sure it's in"
				+ "the same directory as the script")
		feeds = []
		for key in key_arr:
			feeds.append(parse(key))
		return feeds

	def parse_bitbucket(cls, raw, display=True):
		count = 0
		for inst in raw['entries']:
			soup = BeautifulSoup(inst['summary'])
			try:
				if(soup.find('p')):
					n = Notification(inst['title'],
							soup.find('p').text)
				if(not cls.displayed_messages.__contains__(inst['id'])):
					cls.displayed_messages.append(inst['id'])
					if n and display:
						n.show()
						count += 1
						if count > 3:
							return True
			except Exception, e:
				pass
		return True

	def parse_github(cls, raw, display=True):
		count = 0
		for inst in raw['entries']:
			soup = BeautifulSoup(inst['summary'])
			try:
				if(soup.find('blockquote')):
					n = Notification(inst['title'],
							soup.find('blockquote').text)
				else:
					n = Notification(inst['title'],
							'')
				if(not cls.displayed_messages.__contains__(inst['id'])):
					cls.displayed_messages.append(inst['id'])
					if n and display:
						n.show()
						count += 1
						if count > 3:
							return True
			except Exception, e:
				pass
		return True

	def parse_chili(cls, raw, display=True):
		count = 0
		for inst in raw['entries']:
			try:
				n = Notification(inst['title_detail']['value'], inst['author_detail']['name'])
				if(not cls.displayed_messages.__contains__(inst['title'])):
					cls.displayed_messages.append(inst['title'])
					if n and display:
						n.show()
						count += 1
						if count > 3:
							return True
			except Exception, e:
				pass
		return True

	def parse_all(cls):
		feeds = cls.pull_feeds()
		cls.parse_bitbucket(feeds[0])
		cls.parse_github(feeds[1])
		cls.parse_chili(feeds[2])

n = Notifier()
