import logging
import time
import pigpio
import math

from PWMGenerator import AbstractPWMGenerator

# Cheap RC cars have 3-state steering, which requires 2 GPIO pins to control
#
#        | Power Pin  |  Direction Pin |
# -------|------------|----------------|
# Left:  |     1      |        0       |
# Right: |     1      |        1       |
# Center:|     0      |        0       | 
#
# The center position is unpowered. Handled by a spring mechanism. 
#
class ThreeStateSteering(AbstractPWMGenerator):
    
    def __init__(self, name, gpio_power_pin, gpio_direction_pin, android_socket):
        self.logger = logging.getLogger("Steering_%s" % gpio_power_pin)

        self.STEP = 20000 # uS
        self.SLEEP = 0.02 # seconds
        
        self.gpio_direction_pin = gpio_direction_pin

        AbstractPWMGenerator.__init__(self, name, gpio_power_pin, 0, self.STEP, android_socket)
        
        self.center_steering()
    
    def center_steering(self):
        self.current_pulse_width = 0
        self.set_duty_cycle(0)
        self.report_device_state()

    def stop_device(self):
        self.center_steering()
    
    def set_duty_cycle(self, pulse_width_us):
        self.set_direction_pin()
        
#        pigpio.set_PWM_dutycycle(self.pin, math.fabs(pulse_width_us))
        self.logger.info("Position = %s" % pulse_width_us)

    # Selects spin direction for the motor. Negative pulse width represents Reverse.
    def set_direction_pin(self):
        if ( self.current_pulse_width > 0):
            pass
            #pigpio.write(self.gpio_direction_pin, 0)
        else:
            pass
            #pigpio.write(self.gpio_direction_pin, 1)
    
    

    def turn_right(self):
        self.increase_duty_cycle()
        self.report_device_state()

    def turn_left(self):
        self.decrease_duty_cycle()
        self.report_device_state()
