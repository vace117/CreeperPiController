#!/usr/bin/python

import pigpio
from curseyou import *


CHANNEL1_PIN = 24
PERIOD = 1300


RANGE = 20000 # uS (max period)
STEP = 300

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


try:
	stdscr = init_curses()

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
