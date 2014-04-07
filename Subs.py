# -*- encoding: utf8 -*-

def getPlatform():
	import platform
	return [platform.system(), platform.release()]