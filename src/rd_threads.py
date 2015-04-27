#--------------------------------------------------------------
# Threads
#--------------------------------------------------------------
import threading, time
from rd_const import CST
from rd_logger import log

class ValveController(threading.Thread):
	""" Valce control thread """
	
	def __init__(self, GPIO, drops):
		log("ValveController : __init__", src="ValveController")
		threading.Thread.__init__(self)
		self.drops = drops
		self.GPIO = GPIO
	
	def run(self):
		log("ValveController : run", src="ValveController")
		
		for delay,size in self.drops:
			log("ValveController : drop (delay {} ; size {})".format(delay, size), src="ValveController")
			time.sleep(delay/1000.0);
			self.GPIO.output(CST.RPI_PIN_VALVE, 1)
			time.sleep(size/1000.0)
			self.GPIO.output(CST.RPI_PIN_VALVE, 0)
		log("ValveController : end run", src="ValveController")

class ReflexController(threading.Thread):
	""" Reflex control thread """
	
	def __init__(self, GPIO, tps_reflex):
		log("ReflexController : __init__", src="ReflexController")
		threading.Thread.__init__(self)
		self.tps_reflex = tps_reflex
		self.GPIO = GPIO
	
	def run(self):
		log("ReflexController : run", src="ReflexController")
		log("ReflexController : wait tps_reflex {}ms".format(self.tps_reflex), src="ReflexController")
		time.sleep(self.tps_reflex/1000.0)
		self.shot()
		log("ReflexController : run end", src="ReflexController")
	
	def shot(self):
		log("ReflexController : shot", src="ReflexController")
		""" Take a picture """
		self.GPIO.output(CST.RPI_PIN_REFLEX, 1)
		time.sleep(0.1)
		self.GPIO.output(CST.RPI_PIN_REFLEX, 0)
		
 	