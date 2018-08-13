import os
from qlib.data import Cache, dbobj
from qlib.net import to

TEST_DIR = os.path.expanduser("~/.config/SwordNode/plugins/Plugins")

def run(cmd, handle=None, package=None):
	if cmd == 'ls':
		res = os.popen('cd %s && ls ' % TEST_DIR).read()
	elif cmd == 'update':
		res = os.popen('cd %s && git add -A && git commit -m "commit 1" && git pull origin master' % TEST_DIR).read()
	elif cmd == 'updateF':
		res = os.popen('cd %s && git add -A && git commit -m "commit 1" && git pull -f origin master' % TEST_DIR).read()
	elif cmd == 'ps':
		res = os.popen("ps aux | grep -v grep").read()
	elif cmd == 'pip':
		if package and ('&' not in package or '|' not in package):
			package = package.split()[0]
		else:
			return "No package !!"

		if not handle:
			return "No handle"

		if handle == "install":
			res = os.popen("pip3 install %s " % package).read()
		elif handle == 'uninstall':
			res = os.popen("pip3 uninstall -y %s " % package).read()
		else:
			return "No !"
	return res



