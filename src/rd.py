#!/bin/python

import threading
import time
import sys
import getopt


#--------------------------------------------------------------
# parameters
#--------------------------------------------------------------
 
# Times
tps_reflex = 1000 # Reflex trigger
 
# Droplets : (delay with last droplet, size of the droplet)
droplets = [
	(0,	50),
	(150, 80),
]

#--------------------------------------------------------------
# LOG
#--------------------------------------------------------------
import logging
import datetime
current_milli_time = lambda: int(round(time.time() * 1000))

class RdFormatter(logging.Formatter):
	converter = datetime.datetime.fromtimestamp
	dt = current_milli_time()
	def formatTime(self, record, datefmt=None):
		return "{0:05}".format(current_milli_time()-self.dt)

		  
# http://sametmax.com/ecrire-des-logs-en-python/
logger = logging.getLogger('rd')
logger.setLevel(logging.DEBUG)
formatter = RdFormatter('[%(asctime)s] %(levelname)-7s : %(message)s')
steam_handler = logging.StreamHandler()
steam_handler.setFormatter(formatter)
logger.addHandler(steam_handler)


#--------------------------------------------------------------
# led controller
#--------------------------------------------------------------

def led(r, o, g):
	logger.debug("LED {} {} {}".format(r, o, g))
	GPIO.output(CST.RPI_PIN_LED_R, int(r))
	GPIO.output(CST.RPI_PIN_LED_O, int(o))
	GPIO.output(CST.RPI_PIN_LED_G, int(g))

#--------------------------------------------------------------
# Valve controller
#--------------------------------------------------------------

def valve_run():
	""" drop a droplet """
	led (1, 1, 0)
	for delay,size in droplets:
		logger.debug("ValveController : drop (delay {} ; size {})".format(delay, size))
		time.sleep(delay/1000.0);
		GPIO.output(CST.RPI_PIN_VALVE, 1)
		time.sleep(size/1000.0)
		GPIO.output(CST.RPI_PIN_VALVE, 0)

#--------------------------------------------------------------
# Reflex controller
#--------------------------------------------------------------
def reflex_run():
	""" Take a picture """
	led (1, 0, 0)
	logger.debug("Reflex shot")
	GPIO.output(CST.RPI_PIN_REFLEX, 1)
	time.sleep(0.2)
	GPIO.output(CST.RPI_PIN_REFLEX, 0)
	led (1, 1, 1)

#--------------------------------------------------------------
# Callback on GPIO start
#--------------------------------------------------------------
def rpi_callback(pin):
	global lock
	if GPIO.input(CST.RPI_PIN_TRIGGER):
		if lock:
			lock = False
			logger.debug("DOWN")
			if option_manual:
				reflex_run()
	else:
		if not lock:
			lock = True
			logger.debug("UP")
			dt = current_milli_time()
			valve_run()
			dt2 = current_milli_time() - dt
			if not option_manual:
				time.sleep((tps_reflex - dt2)/1000.0)
				reflex_run()



#--------------------------------------------------------------
# MAIN
#--------------------------------------------------------------

help = """
  --verbose=<level> : set log level to INFO(default)|DEBUG|WARNING|ERROR
  --loop=<N>        : run N loop(s), default 1, 0 = infinitly
  --fake-gpio       : do not import GPIO but use fake module
  --manual          : take the photo on button release (use INFO level log to get milisec value)
  --help            : display this message
"""

option_verbose = logging.WARNING
option_fake_gpio = False
option_manual = False
option_loop_count = 1

#--------------------------------------------------------------
# START PROGRAM
#--------------------------------------------------------------

# handle arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], "h", ["verbose=", "loop=", "fake-gpio", "manual", "help"])
except getopt.GetoptError as err:
	print err
	print help
	sys.exit(2)
for opt, arg in opts:
	if opt == "--help":
		print help
		sys.exit(2)
	elif opt == "--verbose":
		if arg == "DEBUG":
			option_verbose = logging.DEBUG
		elif arg == "INFO":
			option_verbose = logging.INFO
		elif arg == "WARNING":
			option_verbose = logging.WARNING
		elif arg == "ERROR":
			option_verbose = logging.ERROR
	elif opt == "--fake-gpio":
		option_fake_gpio = True
	elif opt == "--manual":
		option_manual = True
	elif opt == "--loop":
		option_loop_count = int(arg)

# import modules
# TODO : if not option_verbose:
from rd_const import CST
if not option_fake_gpio:
	import RPi.GPIO as GPIO
else:
	from rd_gpio_debug import GPIO

steam_handler.setLevel(option_verbose)
logger.info("START")
stats_min = 0
stats_max = 0
stats_sum = 0

lock = False

try:
	# init RPI
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(CST.RPI_PIN_TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(CST.RPI_PIN_REFLEX, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_VALVE, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_LED_R, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_LED_O, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_LED_G, GPIO.OUT)
	
	led(1, 1, 1)
	
	GPIO.add_event_detect(CST.RPI_PIN_TRIGGER, GPIO.BOTH, rpi_callback, 100)
	
	while True:
		time.sleep(1)
	
except KeyboardInterrupt:
	# Ctrl+C
	logger.warning("user exit")

#except Exception, e:
#	logger.error("Exception occured!")
#	print e
	
finally:
	GPIO.cleanup()


logger.info("END")
