#--------------------------------------------------------------
# Threads
#--------------------------------------------------------------
import threading, time
from rd_const import CST

import logging
logger = logging.getLogger('rd.threads')

class ValveController(threading.Thread):
	""" Valce control thread """
	
	def __init__(self, GPIO, drops):
		logger.debug("ValveController : __init__")
		threading.Thread.__init__(self)
		self.drops = drops
		self.GPIO = GPIO
	
	def run(self):
		logger.debug("ValveController : run")
		
		for delay,size in self.drops:
			logger.info("ValveController : drop (delay {} ; size {})".format(delay, size))
			time.sleep(delay/1000.0);
			self.GPIO.output(CST.RPI_PIN_VALVE, 1)
			time.sleep(size/1000.0)
			self.GPIO.output(CST.RPI_PIN_VALVE, 0)
		logger.debug("ValveController : end run")

class ReflexController(threading.Thread):
	""" Reflex control thread """
	
	def __init__(self, GPIO, tps_reflex, option_manual):
		logger.debug("ReflexController : __init__")
		threading.Thread.__init__(self)
		self.tps_reflex = tps_reflex
		self.GPIO = GPIO
		self.option_manual = option_manual
	
	def run(self):
		logger.debug("ReflexController : run")
		if self.option_manual:
			self.GPIO.wait_for_edge(CST.RPI_PIN_TRIGGER, self.GPIO.FALLING)
			logger.debug("ReflexController : manual shot")
		else:
			logger.debug("ReflexController : wait tps_reflex {}ms".format(self.tps_reflex))
			time.sleep(self.tps_reflex/1000.0)
		self.shot()
		logger.debug("ReflexController : run end")
	
	def shot(self):
		logger.info("ReflexController : shot")
		""" Take a picture """
		self.GPIO.output(CST.RPI_PIN_REFLEX, 1)
		time.sleep(0.1)
		self.GPIO.output(CST.RPI_PIN_REFLEX, 0)
		
 	