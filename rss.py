#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks github and notifies if there are new commits
import pynotify
import feedparser
import datetime
if not pynotify.init("Version Control Notifier"):
	exit()

def pull_feeds():
	#Bitbucket feed
	feed =feedparser.parse("https://bitbucket.org/rbrown/atom/feed?token=0ab0af15b07352b1596a30bed1293615")
	#Github feeds
	feed2 =feedparser.parse("https://github.com/ryansb.private.actor.atom?token=cae0b3520b731518fcc0f2fc683cae31")
	return [feed, feed2]

#n = pynotify.Notification("Title", "Message")
#n.show()
