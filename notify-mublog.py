#!/usr/bin/env python

import sys
import urllib, urllib2

import githook


CONFIG_URL = 'hooks.mublogurl'
CONFIG_USER = 'hooks.mubloguser'
CONFIG_PASS = 'hooks.mublogpass'
CONFIG_COMMIT_URL = 'hooks.commiturl'
SHORTEN_URL = r'http://is.gd/api.php?longurl=%s'

def make_tiny_url(url):
    u = urllib2.urlopen(SHORTEN_URL % url)
    return u.read()


def post(opener, url, status):
    u = opener.open(url, urllib.urlencode({'status': status}))
    u.read()
    u.close()


if __name__ == '__main__':
    url = githook.get_config(CONFIG_URL)

    # make urlopen do basic auth
    auth_hand = urllib2.HTTPBasicAuthHandler(
	urllib2.HTTPPasswordMgrWithDefaultRealm())
    auth_hand.add_password(user=githook.get_config(CONFIG_USER),
			   passwd=githook.get_config(CONFIG_PASS),
			   realm=None,
			   uri=url)
    opener = urllib2.build_opener(auth_hand)

    commit_url = githook.get_config(CONFIG_COMMIT_URL)

    data = githook.parse_input(sys.stdin)
    for d in data:
	for rev in githook.get_revisions(d['old'], d['new']):
	    msg = 'commit: ' + rev['message']
	    link = make_tiny_url(commit_url % rev['id'])

	    avail = 140 - len(link) - 1
	    if len(msg) > avail:
		msg = msg[:avail-3] + '...'
	
	    status = '%s %s' % (msg, link)

	    post(opener, url, status)

