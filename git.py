#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks github and notifies if there are new commits
import pynotify
import urllib2
import json
import datetime
if not pynotify.init("Version Control Notifier"):
	exit()

def get_repos(user):
	watched = urllib2.urlopen('https://github.com/api/v2/json/repos/watched/'+user).read() # gets all watched repos by a user
	return json.loads(watched)['repositories'] # dictionary of all watched repos

def get_author(iuser, irepo):
	print iuser, irepo
	iuser = 'ryansb'
	irepo = 'vc_notify'
	url = 'http://github.com/api/v2/json/commits/list/{user}/{repo}/master'
	act = urllib2.urlopen(url.format(user=iuser, repo=irepo)).read() # gets all watched repos by a user
	#act = urllib2.urlopen('http://github.com/api/v2/json/commits/list/ryansb/vc_notify/master').read() # gets all watched repos by a user
	#http://github.com/api/v2/json/commits/list/ryansb/vc_notify/master
	#['commits'][0]['author']['name']
	return json.loads(act)['commits'][0]['author']['name']
	#to find the branches of a repo:
	#curl http://github.com/api/v2/json/repos/show/schacon/ruby-git/branches


repos = get_repos('ryansb')
#print datetime.datetime.now()
for i in repos:
	print i['name']
	print i['pushed_at']
	print i['owner']
	print get_author(i['owner'], i['name'])

#n = pynotify.Notification(rdict['repository']['name'], ['repository']['pushed_at'])
#n.show()

#n = pynotify.Notification("Title", "Message")
#n.show()
"""Contents of the repository dictionary for ryansb/project_euler
{'repository':
	{'fork': False,
	'has_wiki': True,
	'description': 'My work on Project Euler,
	figured it was worth a shot',
	'has_downloads': True,
	'url': 'https://github.com/ryansb/project_euler',
	'created_at': '2011/05/04 12:21:26 -0700',
	'private': False,
	'name': 'project_euler',
	'pushed_at': '2011/05/05 15:40:44 -0700',
	'owner': 'ryansb',
	'watchers': 2,
	'open_issues': 0,
	'has_issues': True,
	'forks': 1,
	'homepage': '',
	'size': 108}
}

Contents of the branch dictionary for ryansb/project_euler/branches
{'branches':
	{'master': '4cd453ad02de472ef1b305aa57c450858dad0e14'}
}
"""
