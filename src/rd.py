#!/bin/python

debug = True

import threading
import time
import sys
import getopt

from rd_logger import log
from rd_const import CST


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

if not debug:
	import RPi.GPIO as GPIO
else:
	from rd_gpio_debug import GPIO

from rd_threads import ValveController, ReflexController


#--------------------------------------------------------------
# MAIN
#--------------------------------------------------------------

# TTTTTT    OOOO    DDDDD     OOOO
#   TT     OO  OO   D    D   OO  OO
#   TT     OO  OO   D    D   OO  OO
#   TT     OO  OO   D    D   OO  OO
#   TT      OOOO    DDDDD     OOOO 

def get_parameters(argv):
	try:
		opts, args = getopt.getopt(argv,"h",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg


#--------------------------------------------------------------
# START PROGRAM
#--------------------------------------------------------------

# handle arguments
get_parameters(sys.argv[1:])

log("START")

# Valve controller
valve_thread = ValveController(GPIO, drops)

# Reflex controller
reflex_controller = ReflexController(GPIO, tps_reflex)

# init RPI
GPIO.setmode(GPIO.BCM)
GPIO.setup(CST.RPI_PIN_TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CST.RPI_PIN_VALVE, GPIO.OUT)
GPIO.setup(CST.RPI_PIN_REFLEX, GPIO.OUT)
GPIO.setup(CST.RPI_PIN_LED1, GPIO.OUT)

# Wait for start button
log("Wait for start button")
GPIO.wait_for_edge(CST.RPI_PIN_TRIGGER, GPIO.FALLING)

# let's go
log("launch threads")
valve_thread.start()
reflex_controller.start()

# Fin du traitement
log("wait threads join")
valve_thread.join()
reflex_controller.join()

GPIO.cleanup()

log("END")
