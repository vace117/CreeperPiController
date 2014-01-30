import logging
import time
import pigpio

from PWMGenerator import PWMGenerator

# Use this class to drive a standard servo that functions in the range of 500-2500uS
#
class Servo(PWMGenerator):
    
    def __init__(self, name, gpio_pin, min_pos, max_pos):
        self.logger = logging.getLogger("Servo_%s" % gpio_pin)

        self.STEP = 10 # uS
        self.SLEEP = 0.02 # seconds


        PWMGenerator.__init__(self, name, gpio_pin, min_pos, max_pos)
        
        # Calculated center position in uS
        self.current_pulse_width = 0
        self.center_servo()
    
    def center_position(self):
        exact_position = self.min + ((self.max - self.min)/2)
        return (exact_position / self.STEP) * self.STEP 
    
    def center_servo(self):
        self.move_servo(self.center_position())

    def stop_device(self):
        self.center_servo()
        time.sleep(1)
        self.move_servo(0)
    
    def set_duty_cycle(self, pulse_width_us):
#        pigpio.set_servo_pulsewidth(self.pin, pulse_width_us)
        self.logger.info("Position = %s" % pulse_width_us)
    

    # Alias some functions from the base class        
    move_servo = PWMGenerator.smooth_set_duty_cycle
    decrease_servo_position = PWMGenerator.decrease_duty_cycle
    increase_servo_position = PWMGenerator.increase_duty_cycle
        
