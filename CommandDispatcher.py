from Servos import Servo
from BiDirectionalMotor import BiDirectionalMotor
from ThreeStateSteering import ThreeStateSteering
from thread import start_new_thread

import pigpio
#pigpio.start()

       
class CommandDispatcher:

    def __init__(self, android_socket):
        self.devices = {\
                       "pan_tilt_azimuth"      : Servo("AZIMUTH", 4, 600, 2400, android_socket), \
                       "pan_tilt_inclination"  : Servo("INCLINATION", 17, 1200, 2400, android_socket), \
                       "rear_drive_motor"      : BiDirectionalMotor("REAR_MOTOR", 21, 23, 5000, 20000, android_socket), \
                       "front_steering"        : ThreeStateSteering("FRONT_STEERING", 24, 25, android_socket) \
                       }
        
        self.android_socket = android_socket
        
    def process_command(self, data):
        if data == "LOOK_LEFT":
            self.dispath_to_device("pan_tilt_azimuth", "decrease_servo_position")
        elif data == "LOOK_RIGHT":
            self.dispath_to_device("pan_tilt_azimuth", "increase_servo_position")
        elif data == "LOOK_DOWN":
            self.dispath_to_device("pan_tilt_inclination", "increase_servo_position")
        elif data == "LOOK_UP":
            self.dispath_to_device("pan_tilt_inclination", "decrease_servo_position")
        elif data == "LOOK_CENTER":
            self.dispath_to_device("pan_tilt_azimuth", "center_servo")
            self.dispath_to_device("pan_tilt_inclination", "center_servo")
        
        elif data == "ACCELERATE":
            self.dispath_to_device("rear_drive_motor", "speed_up")
        elif data == "REVERSE_ACCELERATE":
            self.dispath_to_device("rear_drive_motor", "slow_down")
        elif data == "STOP":
            self.dispath_to_device("rear_drive_motor", "stop_motor")

        elif data == "WHEELS_LEFT":
            self.dispath_to_device("front_steering", "turn_left")
        elif data == "WHEELS_RIGHT":
            self.dispath_to_device("front_steering", "turn_right")
    
    
    # Executes the given method on the given servo in a new thread
    #
    def dispath_to_device(self, servo_name, method_name):
        servo = self.devices[servo_name]
        start_new_thread( getattr(servo, method_name), () )
            
    def stop_all_devices(self):
        for device in self.devices.values():
            device.stop_device()
        
        #pigpio.stop()
    
