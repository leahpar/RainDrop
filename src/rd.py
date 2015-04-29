#!/bin/python

import threading
import time
import sys
import getopt


#--------------------------------------------------------------
# parameters
#--------------------------------------------------------------
 
# Times
tps_reflex = 650		# Reflex trigger
 
# Drops : (delay with last drop, size of the drop)
drops = [
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
		# ct = self.converter(record.created)
		# if datefmt:
			# s = ct.strftime(datefmt)
		# else:
			# t = ct.strftime("%Y-%m-%d %H:%M:%S")
			# s = "%s.%03d" % (t, record.msecs)
		# return s

		  
# http://sametmax.com/ecrire-des-logs-en-python/
logger = logging.getLogger('rd')
logger.setLevel(logging.DEBUG)
formatter = RdFormatter('[%(asctime)s] %(levelname)-7s : %(message)s')
steam_handler = logging.StreamHandler()
steam_handler.setFormatter(formatter)
logger.addHandler(steam_handler)

#--------------------------------------------------------------
# MAIN
#--------------------------------------------------------------

help = """
  --verbose=<level> : set log level to INFO|DEBUG|WARNING(default)|ERROR
  --fake-gpio       : do not import GPIO but use fake module
  --manual          : take the photo on button release (use INFO level log to get milisec value)
  --help            : display this message
"""

option_verbose = logging.WARNING
option_fake_gpio = False
option_manual = False

#--------------------------------------------------------------
# START PROGRAM
#--------------------------------------------------------------

# handle arguments
try:
	opts, args = getopt.getopt(sys.argv[1:], "h", ["verbose=", "fake-gpio", "manual", "help"])
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

# import modules
# TODO : if not option_verbose:
from rd_const import CST
if not option_fake_gpio:
	import RPi.GPIO as GPIO
else:
	from rd_gpio_debug import GPIO
from rd_threads import ValveController, ReflexController

steam_handler.setLevel(option_verbose)
logger.info("START")

# Valve controller
valve_thread = ValveController(GPIO, drops)

# Reflex controller
reflex_controller = ReflexController(GPIO, tps_reflex, option_manual)

try:
	# init RPI
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(CST.RPI_PIN_TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(CST.RPI_PIN_VALVE, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_REFLEX, GPIO.OUT)
	GPIO.setup(CST.RPI_PIN_LED1, GPIO.OUT)

	# Wait for start button
	logger.info("Wait for start button")
	GPIO.wait_for_edge(CST.RPI_PIN_TRIGGER, GPIO.RISING)
	
	# let's go
	logger.debug("launch threads")
	valve_thread.start()
	reflex_controller.start()

	# Fin du traitement
	logger.debug("wait threads join")
	valve_thread.join()
	reflex_controller.join()
	
except KeyboardInterrupt:
	# Ctrl+C
	logger.warning("user exit")

except:
	logger.error("Exception occured!")
	
finally:
	GPIO.cleanup()

logger.info("END")
