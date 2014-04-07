# -*- encoding: utf8 -*-
import ctypes, time, platform, re

class LastInputInfo(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),('dwTime', ctypes.c_ulong)]

def getCurrentJobXP(vista=True):
	# get information about current active window
	# including: window title, image name
	# for Windows XP and 32-bit environment

	# required DLLs
	user32 = ctypes.windll.LoadLibrary('user32.dll')
	kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
	psapi = ctypes.windll.LoadLibrary('psapi.dll')
	# required constants
	BUFFER_LENGTH = 1024
	SYNCHRONIZE = 0x00100000L
	PROCESS_QUERY_INFORMATION = 0x0400
	PROCESS_VM_READ = 0x0010
	# some buffers
	title = ctypes.create_unicode_buffer(BUFFER_LENGTH)
	image = ctypes.create_unicode_buffer(BUFFER_LENGTH)
	length = ctypes.c_ulong(BUFFER_LENGTH)
	plength = ctypes.pointer(length)
	# start working!
	user32.GetWindowTextW(user32.GetForegroundWindow(), title, ctypes.sizeof(title))
	pid = ctypes.c_int(0)
	ppid = ctypes.pointer(pid)
	user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ppid)
	hProcess = kernel32.OpenProcess(SYNCHRONIZE | PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, True, pid)
	result = 0
	result = psapi.GetModuleFileNameExW(hProcess, None, image, ctypes.sizeof(image))
	if result == 0:
		print kernel32.GetLastError()
	# return results
	return {'title': title.value, 'image': image.value}

def getCurrentJobVista():
	# get information about current active window
	# including: window title, image name
	# only supported in Windows Vista and above

	# required DLLs
	user32 = ctypes.windll.LoadLibrary('user32.dll')
	kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')
	psapi = ctypes.windll.LoadLibrary('psapi.dll')
	# required constants
	BUFFER_LENGTH = 1024
	SYNCHRONIZE = 0x00100000L
	PROCESS_QUERY_INFORMATION = 0x0400
	PROCESS_VM_READ = 0x0010
	# some buffers
	title = ctypes.create_unicode_buffer(BUFFER_LENGTH)
	image = ctypes.create_unicode_buffer(BUFFER_LENGTH)
	length = ctypes.c_ulong(BUFFER_LENGTH)
	plength = ctypes.pointer(length)
	# start working!
	user32.GetWindowTextW(user32.GetForegroundWindow(), title, ctypes.sizeof(title))
	pid = ctypes.c_int(0)
	ppid = ctypes.pointer(pid)
	user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ppid)
	hProcess = kernel32.OpenProcess(SYNCHRONIZE | PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, True, pid)
	result = 0
	result = kernel32.QueryFullProcessImageNameW(hProcess, 0, image, plength)
	if result == 0:
		print kernel32.GetLastError()
	# return results
	return {'title': title.value, 'image': image.value}

def isIdle():
	# judge if system is idle now
	# accuracy is 500ms

	# required DLLs
	user32 = ctypes.windll.LoadLibrary('user32.dll')
	kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')

	lastinput = LastInputInfo()
	lastinput.cbSize = ctypes.sizeof(lastinput)
	plastinput = ctypes.pointer(lastinput)
	user32.GetLastInputInfo.argtypes = [ctypes.POINTER(LastInputInfo)]
	user32.GetLastInputInfo(plastinput)
	return kernel32.GetTickCount64() - lastinput.dwTime > 500