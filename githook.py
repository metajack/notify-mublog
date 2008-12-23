# githook.py

"""Small library to handle interaction with Git for notification scripts.
"""

from datetime import datetime
import re
import subprocess

_EMAIL_RE = re.compile("^(.*) <(.*)>$")

def parse_input(f):
    """Parse the hook input data from Git.
    """

    data = []
    for line in f.readlines():
	old, new, ref = line.strip().split(' ')
	data.append({'old': old, 'new': new, 'ref': ref})

    return data

def git(*args):
    proc = subprocess.Popen(['git'] + list(args), stdout=subprocess.PIPE)
    return proc.stdout.read()

def get_config(name):
    return git('config', name).strip()
    
def get_revisions(old, new):
    output = git('rev-list', '--pretty=medium',
		 '%s..%s' % (old, new))
    sections = output.split('\n\n')[:-1]

    revisions = []
    s = 0
    while s < len(sections):
	lines = sections[s].split('\n')
	    
	# first line is 'commit HASH\n'
	props = {'id': lines[0].strip().split(' ')[1]}
	    
	# read the header
	for l in lines[1:]:
	    key, val = l.split(' ', 1)
	    props[key[:-1].lower()] = val.strip()

	# read the commit message
	props['message'] = sections[s+1]

	# use github time format
	basetime = datetime.strptime(props['date'][:-6], "%a %b %d %H:%M:%S %Y")
	tzstr = props['date'][-5:]
	props['date'] = basetime.strftime('%Y-%m-%dT%H:%M:%S') + tzstr

	# split up author
	m = _EMAIL_RE.match(props['author'])
	if m:
	    props['name'] = m.group(1)
	    props['email'] = m.group(2)
	else:
	    props['name'] = 'unknown'
	    props['email'] = 'unknown'
	del props['author']
	
	revisions.append(props)
	s += 2
	
    return revisions
