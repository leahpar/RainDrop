#--------------------------------------------------------------
# Fake GPIO class for debug
#--------------------------------------------------------------

import time

from rd_logger import log

class GPIO:
	""" GPIO Debug class """
	BCM = "GPIO.BCM"
	PUD_DOWN = "GPIO.PUD_DOWN"
	IN = "GPIO.IN"
	OUT = "GPIO.OUT"
	FALLING = "GPIO.FALLING"
	
	def __getattr__(self, name):
		log("[{}] Get attr {}".format(time.time(), name), src="GPIO")
		
	def __setattr__(self, name, value):
		log("Set attr {} = {}".format(name, value), src="GPIO")
		
	@staticmethod
	def output(pin, value):
		log("Set pin {} to value {}".format(pin, value), src="GPIO")
	
	@staticmethod
	def setmode(mode):
		log("Set mode to {}".format(mode), src="GPIO")
	
	@staticmethod
	def setup(pin, mode, pull_up_down="none"):
		log("Setup pin {} to mode {} (pud = {})".format(pin, mode, pull_up_down), src="GPIO")
	
	@staticmethod
	def wait_for_edge(pin, edge):
		log("Wait for edge {} on pin {}...".format(edge, pin), src="GPIO")
		time.sleep(1)
		log("...so here you are!", src="GPIO")

	@staticmethod
	def cleanup():
		log("Cleanup", src="GPIO")
		
