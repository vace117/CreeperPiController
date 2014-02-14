#!/usr/bin/python
#
# Set's all specified GPIO pins to LOW

import pigpio
import sys, traceback, time


def init_pin(pin):
	pigpio.start()
	pigpio.set_mode(pin, pigpio.OUTPUT)

def set_pin_to(pin, value):
	pigpio.write(pin, value)
	print("GPIO Pin %s set to %s    " % (pin, value))
		

if ( len(sys.argv) < 2 ):
	print "Usage: ./clear_pins.py p1 p2 p3 ... etc\n"
	sys.exit(-1)

try:
	for arg in sys.argv[1:]:
		pin = int(arg)
		init_pin(pin)
		set_pin_to(pin, 0)
	
	
except:
	etype, value, tb = sys.exc_info()
	traceback.print_exception(etype, value, tb)
	
finally:
	print "Cleaning up..."
	time.sleep(0.1)
	pigpio.stop()
	
