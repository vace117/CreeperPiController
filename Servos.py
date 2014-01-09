import logging
import time
from thread import start_new_thread

import pigpio
pigpio.start()

class Servo:
    
    STEP = 15
    
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
        
    def move_servo(self, position):
        pigpio.set_servo_pulsewidth(self.pin, position)
        self.logger.info("Position = %s" % position)
        self.android_socket.thread_safe_push("%s:%s\n" % (self.name, position) )

    def decrease_servo_position(self):
        if ( (self.current_position - self.STEP) >= self.min ):
            self.current_position -= self.STEP
            self.move_servo(self.current_position)
        
    def increase_servo_position(self):
        if ( (self.current_position + self.STEP) <= self.max ):
            self.current_position += self.STEP
            self.move_servo(self.current_position)
    
    def stop_servo(self):
        self.move_servo(self.center_position())
        time.sleep(0.5)
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
        elif data == "LOOK_RIGHT":
            start_new_thread( self.servos["pan_tilt_azimuth"].increase_servo_position, () )
        elif data == "LOOK_UP":
            start_new_thread( self.servos["pan_tilt_inclination"].increase_servo_position, () )
        elif data == "LOOK_DOWN":
            start_new_thread( self.servos["pan_tilt_inclination"].decrease_servo_position, () )
            
    def stop_all_servos(self):
        for servo in self.servos.values():
            servo.stop_servo()
        
        pigpio.stop()
    
