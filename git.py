#!/usr/bin/env python
# Author: Ryan Brown
# Description: checks github and notifies if there are new commits
import pynotify
import urllib2
import json
import datetime
if not pynotify.init("Version Control Notifier"):
	exit()

full_repo = urllib2.urlopen('https://github.com/api/v2/json/repos/show/ryansb/project_euler').read() # gets repo info
watched = urllib2.urlopen('https://github.com/api/v2/json/repos/watched/ryansb').read() # gets repo info
repo_branches = urllib2.urlopen('https://github.com/api/v2/json/repos/show/ryansb/project_euler/branches').read()
rdict = json.loads(full_repo)
bdict = json.loads(repo_branches)
wdict = json.loads(watched) # dictionary of all watched repos


#print datetime.datetime.now()

n = pynotify.Notification(rdict['repository']['name'], rdict['repository']['pushed_at'])
n.show()

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
#http;//github.com/api/v2/json/repos/watched/ryansb returns all the repos I watch
