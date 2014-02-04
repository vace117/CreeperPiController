import logging
import pigpio

from PWMGenerator import PWMGenerator

# Defining the enum construct, since Python doesn't have one
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

DIRECTION = Enum(["FORWARD", "REVERSE"])


# This class is used to drive a bi-directional motor
# 3 pins are required for a motor:
#    - gpio_pwm_pin: The pin that will deliver the PWM power signal
#    - gpio_forward_pin = ~gpio_reverse_pin: 
#
#    gpio_forward_pin | gpio_reverse_pin |     Result   |
#   ------------------|------------------|--------------|
#            1        |        0         | Forward spin |
#            0        |        1         | Reverse spin |
#
#    This can obviously be achieved with just one pin, but then an inverter 
#    would be required. Unfortunately inverters come only in DIP packages,
#    so I am choosing to use up an extra GPIO pin in order to save PCB board space
#
class BiDirectionalMotor(PWMGenerator):
    def __init__(self, name, gpio_pwm_pin, gpio_forward_pin, gpio_reverse_pin, min_pos, max_pos):
        self.logger = logging.getLogger("Motor_%s" % gpio_pwm_pin)

        self.STEP = 100
        self.SLEEP = 0.01

        # Common init code
        PWMGenerator.__init__(self, name, gpio_pwm_pin, min_pos, max_pos)

        # Power up with forward motor direction set at minimum power 
        self.direction = DIRECTION.FORWARD
        self.current_pulse_width = self.min
        
        self.forward_pin = gpio_forward_pin
        self.reverse_pin = gpio_reverse_pin

        
        self.smooth_set_duty_cycle(self.current_pulse_width)
        
        
    def _pigpio_init_pwm(self):
        PWMGenerator._pigpio_init_pwm(self)
#        pigpio.set_mode(self.forward_pin, pigpio.OUTPUT)
#        pigpio.set_mode(self.reverse_pin, pigpio.OUTPUT)

    
    def set_duty_cycle(self, pulse_width_us):
        
        self.set_motor_direction_pins()
        
#        pigpio.set_PWM_dutycycle(self.pin, pulse_width_us)
        
        speed_str = pulse_width_us
        if ( self.STEP < 0 ): speed_str = "-" + str(pulse_width_us)
        
        self.logger.info("Motor Speed = %s" % speed_str)

    # Smoothly cycles the motor down to minimum power
    def stop_motor(self):
        self.__smooth_set_duty_cycle(self.min)

    # Turns off all power to the motor 
    def stop_device(self):
        self.__set_duty_cycle(0)
        
    # Selects spin direction for the motor. See the class comment for explanation
    def set_motor_direction_pins(self):
        if ( DIRECTION.FORWARD == self.get_current_direction() ):
            pass
            #pigpio.write(self.forward_pin, 1)
            #pigpio.write(self.reverse_pin, 0)
        else:
            pass
            #pigpio.write(self.forward_pin, 0)
            #pigpio.write(self.reverse_pin, 1)
    
    # Get current motor spin direction. Negative STEP values indicate Reverse
    def get_current_direction(self):
        return DIRECTION.FORWARD if self.STEP >= 0 else DIRECTION.REVERSE
    
    # Negating current STEP value reverses direction
    def reverse_direction(self):
        self.STEP = -self.STEP
        
    # If power decrease fails, we check if we are at the minimum boundary, and we try again
    # with reversed direction
    def decrease_duty_cycle(self):
        if ( not PWMGenerator.decrease_duty_cycle(self) ):
            if ( self.current_pulse_width == self.min and self.get_current_direction() == DIRECTION.FORWARD ):
                self.reverse_direction()
                self.decrease_duty_cycle()
    
    # If power increase fails, we check if we are at the maximum boundary, and we try again
    # with reversed direction
    def increase_duty_cycle(self):
        if ( not PWMGenerator.increase_duty_cycle(self) ):
            if ( self.current_pulse_width == self.max and self.get_current_direction() == DIRECTION.REVERSE ):
                self.reverse_direction()
                self.increase_duty_cycle()
                
    def print_servo_position(self, android_socket):
        if ( self.get_current_direction() == DIRECTION.FORWARD ):
            android_socket.push("%s:%s\n" % (self.name, self.current_pulse_width))
        else:
            android_socket.push("%s:-%s\n" % (self.name, self.current_pulse_width))
                

    # Alias some functions from the base class        
    speed_up = increase_duty_cycle
    slow_down = decrease_duty_cycle
        
