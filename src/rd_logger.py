#--------------------------------------------------------------
# Log functions
# Needs var : dt, lock
#--------------------------------------------------------------
import time
import threading

current_milli_time = lambda: int(round(time.time() * 1000))
dt = current_milli_time()
lock = threading.RLock()

class bcolors:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def log(str, src="default"):
	
	with lock:
		if src == "ReflexController":
			color = bcolors.GREEN
		elif src == "ValveController":
			color = bcolors.YELLOW
		elif src == "GPIO":
			color = bcolors.RED
		else:
			color = bcolors.ENDC
		print(color + "[{0:05}] ".format(current_milli_time()-dt) + str + bcolors.ENDC)
