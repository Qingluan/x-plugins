import os
from qlib.data import Cache, dbobj
from qlib.net import to

TEST_DIR = os.path.expanduser("~/.config/SwordNode/plugins/Plugins")

def run(cmd):
	if cmd == 'ls':
		res = os.popen('cd %s && ls ' % TEST_DIR).read()
	elif cmd == 'update':
		res = os.popen('cd %s && git add -A && git commit -m "commit 1" && git pull origin master' % TEST_DIR).read()
	elif cmd == 'updateF':
		res = os.popen('cd %s && git add -A && git commit -m "commit 1" && git pull -f origin master' % TEST_DIR).read()
	elif cmd == 'ps':
		res = os.popen("ps aux | grep -v grep").read()

	return res



