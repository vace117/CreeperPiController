from Servos import Servo
from BiDirectionalMotor import BiDirectionalMotor
from thread import start_new_thread

import pigpio
#pigpio.start()

       
class CommandDispatcher:

    def __init__(self, android_socket):
        self.devices = {\
                       "pan_tilt_azimuth"      : Servo("AZIMUTH", 4, 600, 2400), \
                       "pan_tilt_inclination"  : Servo("INCLINATION", 17, 1200, 2400), \
                       "rear_drive_motor"      : BiDirectionalMotor("REAR_MOTOR", 21, 23, 24, 5000, 20000) \
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
    
    
    # Executes the given method on the given servo in a new thread, then prints servo state
    # into the network socket from the main thread.
    #
    # PROBLEM: This code does not wait for the thread to return, so we don't know what we are actually printing
    #
    def dispath_to_device(self, servo_name, method_name):
        servo = self.devices[servo_name]
        start_new_thread( getattr(servo, method_name), () )
        servo.print_servo_position(self.android_socket)
            
    def stop_all_devices(self):
        for servo in self.devices.values():
            servo.stop_device()
        
        #pigpio.stop()
    
