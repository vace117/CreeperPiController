#!/usr/bin/python

import pigpio
import sys, traceback, time

from curseyou import *


def init_pin(pin):
	pigpio.start()
	pigpio.set_mode(PIN, pigpio.OUTPUT)

def set_pin_to(pin, value):
	pigpio.write(pin, value)
	print_at(5, 0, "Pin %s set to %s    " % (pin, value))
		

if ( len(sys.argv) < 2 ):
	print "Usage: ./set_pin.py pin_number [0/1]\n"
	sys.exit(-1)

try:
	PIN = int(sys.argv[1])
	VALUE = int(sys.argv[2])

	stdscr = init_curses()

	println("\nPress Enter to flip between values")
	init_pin(PIN)
	set_pin_to(PIN, VALUE)
	
	while True:
		key = stdscr.getch()
		if key == 10:
			set_pin_to(PIN, int(not bool(pigpio.read(PIN))))
	
	
	
except:
	etype, value, tb = sys.exc_info()
	traceback.print_exception(etype, value, tb)
	
finally:
	restore_terminal()
	print "Cleaning up..."
	time.sleep(0.1)
	pigpio.stop()
	
