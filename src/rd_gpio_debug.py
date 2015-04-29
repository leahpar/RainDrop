#--------------------------------------------------------------
# Fake GPIO class for debug
#--------------------------------------------------------------

import time, random, logging
logger = logging.getLogger('rd.gpio')

class GPIO:
	""" GPIO Debug class """
	BCM = "GPIO.BCM"
	PUD_DOWN = "GPIO.PUD_DOWN"
	PUD_UP = "GPIO.PUD_UP"
	IN = "GPIO.IN"
	OUT = "GPIO.OUT"
	FALLING = "GPIO.FALLING"
	RISING = "GPIO.RISING"
	
	def __getattr__(self, name):
		logger.debug("Get attr {}".format(name))
		
	def __setattr__(self, name, value):
		logger.debug("Set attr {} = {}".format(name, value))
		
	@staticmethod
	def output(pin, value):
		logger.debug("Set pin {} to value {}".format(pin, value))
	
	@staticmethod
	def setmode(mode):
		logger.debug("Set mode to {}".format(mode))
	
	@staticmethod
	def setup(pin, mode, pull_up_down="none"):
		logger.debug("Setup pin {} to mode {} (pud = {})".format(pin, mode, pull_up_down))
	
	@staticmethod
	def wait_for_edge(pin, edge):
		r = (random.randrange(500, 1500))
		logger.debug("Wait for edge {} on pin {} ({}ms)...".format(edge, pin, r))
		time.sleep(r/1000.0)
		logger.debug("...so here you are!")

	@staticmethod
	def cleanup():
		logger.debug("Cleanup")
		
