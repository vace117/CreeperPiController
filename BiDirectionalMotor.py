import logging
import math
import pigpio

from PWMGenerator import AbstractPWMGenerator

# This class is used to drive a bi-directional motor
# 2 pins are required for a motor:
#    - gpio_pwm_pin: The pin that will deliver the PWM power signal
#    - gpio_direction_pin: 0 = forward, 1 = reverse 
#
class BiDirectionalMotor(AbstractPWMGenerator):
    def __init__(self, name, gpio_pwm_pin, gpio_direction_pin, min_pos, max_pos, android_socket):
        self.logger = logging.getLogger("Motor_%s" % gpio_pwm_pin)

        self.STEP = 2500
        self.SLEEP = 0.1

        self.gpio_direction_pin = gpio_direction_pin

        # Common init code
        AbstractPWMGenerator.__init__(self, name, gpio_pwm_pin, min_pos, max_pos, android_socket)

        # Power up with forward motor direction set at minimum power. Positive pulse width represents Forward.
        self.current_pulse_width = self.min

        self.set_motor_direction_pins()
        self.smooth_set_duty_cycle(self.current_pulse_width)
        
        
    def pigpio_init_pwm(self):
        AbstractPWMGenerator.pigpio_init_pwm(self)
        pigpio.set_mode(self.gpio_direction_pin, pigpio.OUTPUT)
    
    def set_duty_cycle(self, pulse_width_us):
        
        self.set_motor_direction_pins()
        
        if ( math.fabs(pulse_width_us) == self.min ):
            # If we have reached the bottom of the power range, turn the power off entirely so we don't waste any
            self.logger.info("Shutting down motor") 
            pigpio.set_PWM_dutycycle(self.pin, 0)
        else:
            pigpio.set_PWM_dutycycle(self.pin, math.fabs(pulse_width_us))
        
        self.logger.info("Motor Speed = %s" % pulse_width_us)

    # Smoothly cycles the motor down to minimum power
    def stop_motor(self):
        self.smooth_set_duty_cycle(self.min)

    # Turns off all power to the motor 
    def stop_device(self):
        self.set_duty_cycle(0)
        
    # Selects spin direction for the motor. Negative pulse width represents Reverse.
    def set_motor_direction_pins(self):
        if ( self.current_pulse_width >= 0):
            pigpio.write(self.gpio_direction_pin, 0)
        else:
            pigpio.write(self.gpio_direction_pin, 1)

        self.logger.info("Direction pin set to %s" % pigpio.read(self.gpio_direction_pin))
        
    
    # Negating current STEP value reverses direction
    def reverse_direction(self):
        self.current_pulse_width = -self.current_pulse_width
        
    # If power decrease fails, we check if we are at the minimum boundary, and we try again
    # with reversed direction
    def decrease_duty_cycle(self):
        success = AbstractPWMGenerator.decrease_duty_cycle(self)
        if ( not success ):
            if ( self.current_pulse_width == self.min ):
                self.reverse_direction()
                self.decrease_duty_cycle()
        
        return success
    
    # If power increase fails, we check if we are at the negative min boundary, and we try again
    # with reversed direction
    def increase_duty_cycle(self):
        success = AbstractPWMGenerator.increase_duty_cycle(self)
        if ( not success ):
            if ( -self.current_pulse_width == self.min ):
                self.reverse_direction()
                self.increase_duty_cycle()
        
        return success

    def speed_up(self):
        self.increase_duty_cycle()
        self.report_device_state()
        
    def slow_down(self):
        self.decrease_duty_cycle()
        self.report_device_state()
        
