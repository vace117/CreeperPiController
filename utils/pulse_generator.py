#!/usr/bin/python

import pigpio
import curses

CHANNEL1_PIN = 4
#PERIOD = 5000
PERIOD = 20000


RANGE = 20000 # uS
STEP = 100

pigpio.start()

def init_channel(pin):
	pigpio.set_PWM_frequency(pin, 50)
	println("PWM cycle frequency: %dHz" % pigpio.get_PWM_frequency(pin))
	pigpio.set_PWM_range(pin, RANGE)


def stop_channel(pin):
	pigpio.set_PWM_dutycycle(pin, 0)

def start_channel(pin, duty_cycle_us):
	init_channel(pin)
	set_channel(pin, duty_cycle_us)

def set_channel(pin, duty_cycle_us):
	pigpio.set_PWM_dutycycle(pin, duty_cycle_us)
	print_at(5, 0, "Channel Duty Cycle: %d/%d              " % (PERIOD,RANGE))

def init_curses():
	global stdscr
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)

def restore_terminal():
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()	

def println(str):
	_print(str + "\n")

def _print(str):
	stdscr.addstr(str)
	stdscr.refresh()

def print_at(y,x,str):
	stdscr.addstr(y,x,str)
	stdscr.refresh()

try:
	init_curses()

	println("\nUse UP and DOWN arrows to control the duty cycle")
	start_channel(CHANNEL1_PIN, PERIOD)


	while True:
		key = stdscr.getch()
		if key == curses.KEY_UP:
			if ( PERIOD < RANGE ):
				PERIOD += STEP
				set_channel(CHANNEL1_PIN, PERIOD)
		elif key == curses.KEY_DOWN:
			if ( PERIOD > 0 ):
				PERIOD -= STEP
				set_channel(CHANNEL1_PIN, PERIOD)

finally:
	restore_terminal()
	print "Cleaning up..."
	stop_channel(CHANNEL1_PIN)
	pigpio.stop()
