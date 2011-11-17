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
#from re import split # unused -- agargiulo 11/15/11
from sys import argv
import os

if not init("VC Notify"):
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
		config = cls.read_config()
		for pair in config.items('providers'):
			if pair[0] == 'bitbucket': cls.parse_bitbucket(parse(pair[1]), display=False)
			elif pair[0] == 'github': cls.parse_github(parse(pair[1]), display=False)
		return True

	def read_config(cls):
		#Returns a list of raw version control feeds
		from ConfigParser import SafeConfigParser
		config = SafeConfigParser()
		if len(argv) == 2:
			if len(config.read(argv[1])) == 0:
				print ("Couldn't open keys file, bad argument passed"
					+ "in")
		else:
			keys_path = os.path.abspath(__file__)
			if len(config.read(keys_path.replace('vc_notify.py', 'keys.txt'))) == 0:
				print ("Couldn't find the keys file, make sure it's in"
				+ "the same directory as the script")
		return config

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
				print e
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
				print e
		return True

	def parse_all(cls):
		config = cls.read_config()
		for pair in config.items('providers'):
			if pair[0] == 'bitbucket':
				cls.parse_bitbucket(parse(pair[1]), display=False)
			elif pair[0] == 'github':
				cls.parse_github(parse(pair[1]), display=False)
		return True

n = Notifier()
