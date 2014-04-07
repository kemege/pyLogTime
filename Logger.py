import time, sqlite3
import Subs

def main():
	platform = Subs.getPlatform()
	if platform[0] == 'Windows':
		from ProcessW32 import isIdle
		if platform[1] in ['Vista', '7', '8']:
			from ProcessW32 import getCurrentJobVista as getCurrentJob
		elif platform[1] == 'XP':
			from ProcessW32 import getCurrentJobXP as getCurrentJob
		else:
			print 'Unsupported Windows version: %s %s'%(platform[0], platform[1])
			return
	for x in xrange(1,20):
		print getCurrentJob()
		print isIdle()
		time.sleep(1)

if __name__ == '__main__':
	main()