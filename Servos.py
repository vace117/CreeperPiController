import logging
import time
import pigpio

from PWMGenerator import AbstractPWMGenerator

# Use this class to drive a standard servo that functions in the range of 500-2500uS
#
class Servo(AbstractPWMGenerator):
    
    def __init__(self, name, gpio_pin, min_pos, max_pos, android_socket):
        self.logger = logging.getLogger("Servo_%s" % gpio_pin)

        self.STEP = 10 # uS
        self.SLEEP = 0.02 # seconds


        AbstractPWMGenerator.__init__(self, name, gpio_pin, min_pos, max_pos, android_socket)
        
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
        self.set_duty_cycle(0)
    
    def set_duty_cycle(self, pulse_width_us):
#        pigpio.set_servo_pulsewidth(self.pin, pulse_width_us)
        self.logger.info("Position = %s" % pulse_width_us)
    

    def decrease_servo_position(self):
        self.decrease_duty_cycle()
        self.report_device_state()

    def increase_servo_position(self):
        self.increase_duty_cycle()
        self.report_device_state()
        
    # Alias some functions from the base class        
    move_servo = AbstractPWMGenerator.smooth_set_duty_cycle
    
