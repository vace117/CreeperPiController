import logging
import math
import time
from thread import start_new_thread

import pigpio
pigpio.start()

class Servo:
    
    STEP = 40
    SLEEP = 0.02
    
    def __init__(self, name, gpio_pin, min_pos, max_pos, android_socket):
        self.logger = logging.getLogger("Servo_%s" % gpio_pin)
        
        self.android_socket = android_socket
        self.name = name
        
        # GPIO pin to which the servo is connected
        self.pin = gpio_pin
        
        # Pulse widths for the extreme positions of the servo. 
        # These values are specified in uS 
        self.min = min_pos
        self.max = max_pos
        
        # Calculated center position in uS
        self.current_position = self.center_position()
        
        # Init the servo pin and move the servo to the center (neutral) position
        self._pigpio_init_servo()
    
    def center_position(self):
        return self.min + ((self.max - self.min)/2)
    
    def _pigpio_init_servo(self):
        pigpio.set_PWM_frequency(self.pin, 50) # 50Hz pulses
        pigpio.set_PWM_range(self.pin, 20000) # 1,000,000 / 50 = 20,000us for 100% duty cycle
        self.move_servo(self.center_position())
        
    def move_servo(self, new_position):
	old_position = self.current_position
	if (new_position != 0 and math.fabs(old_position - new_position) > self.STEP):
	    if old_position < new_position:
	    	for pos in range(old_position, new_position + self.STEP, self.STEP):
		   pigpio.set_servo_pulsewidth(self.pin, pos)
		   time.sleep(self.SLEEP)
	    if old_position > new_position:
		for pos in range(old_position, new_position - self.STEP, -self.STEP):
                   pigpio.set_servo_pulsewidth(self.pin, pos)
		   time.sleep(self.SLEEP)

        pigpio.set_servo_pulsewidth(self.pin, new_position)

	self.current_position = new_position
        self.logger.info("Position = %s" % new_position)

    def center_servo(self):
        self.move_servo(self.center_position())

    def decrease_servo_position(self):
        if ( (self.current_position - self.STEP) >= self.min ):
            self.move_servo(self.current_position - self.STEP)
        
    def increase_servo_position(self):
        if ( (self.current_position + self.STEP) <= self.max ):
            self.move_servo(self.current_position + self.STEP)
    
    def stop_servo(self):
        self.center_servo()
        time.sleep(1)
        self.move_servo(0)
        

class ServoController:

    def __init__(self, android_socket):
        self.servos = {\
                       "pan_tilt_azimuth" : Servo("AZIMUTH", 4, 700, 2200, android_socket), \
                       "pan_tilt_inclination" : Servo("INCLINATION", 17, 700, 2200, android_socket) \
                       }
        
        self.android_socket = android_socket
        
    def process_command(self, data):
        if data == "LOOK_LEFT":
            start_new_thread( self.servos["pan_tilt_azimuth"].decrease_servo_position, () )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_azimuth"].name, self.servos["pan_tilt_azimuth"].current_position) )
        elif data == "LOOK_RIGHT":
            start_new_thread( self.servos["pan_tilt_azimuth"].increase_servo_position, () )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_azimuth"].name, self.servos["pan_tilt_azimuth"].current_position) )
        elif data == "LOOK_UP":
            start_new_thread( self.servos["pan_tilt_inclination"].increase_servo_position, () )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_inclination"].name, self.servos["pan_tilt_inclination"].current_position) )
        elif data == "LOOK_DOWN":
            start_new_thread( self.servos["pan_tilt_inclination"].decrease_servo_position, () )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_inclination"].name, self.servos["pan_tilt_inclination"].current_position) )
        elif data == "LOOK_CENTER":
	    start_new_thread( self.servos["pan_tilt_azimuth"].center_servo, () )
	    start_new_thread( self.servos["pan_tilt_inclination"].center_servo, () )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_azimuth"].name, self.servos["pan_tilt_azimuth"].current_position) )
            self.android_socket.push("%s:%s\n" % (self.servos["pan_tilt_inclination"].name, self.servos["pan_tilt_inclination"].current_position) )
            
    def stop_all_servos(self):
        for servo in self.servos.values():
            servo.stop_servo()
        
        pigpio.stop()
    
