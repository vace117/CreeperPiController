#!/usr/bin/python

import pigpio
import time
import thread

SERVO1_PIN = 4
SERVO2_PIN = 17

LEFT = 600
RIGHT = 2400
CENTER = LEFT + ((RIGHT - LEFT)/2)

STEP=20
SLEEP=0.01

pigpio.start()

print "LEFT: %d" % LEFT
print "RIGHT: %d" % RIGHT
print "CENTER: %d" % CENTER

def init_servo(pin):
	pigpio.set_PWM_frequency(pin, 50) # 50Hz pulses
	pigpio.set_PWM_range(pin, 20000) # 1,000,000 / 50 = 20,000us for 100% duty cycle
  	move_servo(pin, CENTER, 5)


def move_servo(pin, duty_cycle_us=0, sleep=SLEEP):
	pigpio.set_servo_pulsewidth(pin, duty_cycle_us)
	time.sleep(sleep)

def spin_servo_cw_from(pin, start=LEFT, sleep=SLEEP):
	for duty_cycle_us in range(start, RIGHT+STEP, STEP): 
		move_servo(pin, duty_cycle_us, sleep)

def spin_servo_ccw_from(pin, start=RIGHT, sleep=SLEEP):
        for duty_cycle_us in range(start, LEFT-STEP, -STEP):
                move_servo(pin, duty_cycle_us, sleep)

def stop_servo(pin):
	pigpio.set_servo_pulsewidth(pin, 0)

def test_servo(pin, direction):
	init_servo(pin)

	if direction: 
		spin_servo_cw_from(pin, CENTER)
	else:
		spin_servo_ccw_from(pin, CENTER)

	while True:
		if direction: 
			spin_servo_ccw_from(pin)
		else:
			spin_servo_cw_from(pin)

		if direction: 
			spin_servo_cw_from(pin)
		else:
			spin_servo_ccw_from(pin)


try:

	thread.start_new_thread( test_servo, (SERVO1_PIN, True) )
	thread.start_new_thread( test_servo, (SERVO2_PIN, False) )

	while True:
		pass

finally:
	print "Cleaning up..."
	stop_servo(SERVO1_PIN)
	stop_servo(SERVO2_PIN)
	pigpio.stop()
