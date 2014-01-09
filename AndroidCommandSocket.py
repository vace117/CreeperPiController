#!/usr/bin/python

import asynchat, asyncore, socket
import logging
from Servos import ServoController
from thread import allocate_lock

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

ANDROID_HOST = ("192.168.6.1", 4444)

class AndroidSocket(asynchat.async_chat):
    
    def __init__(self):
        self.logger = logging.getLogger("AndroidSocket")
        
        # Connect to the Android (when we start the async loop - this is asynchronous)
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( ANDROID_HOST )
        
        # Set up input buffer and define message terminator
        self.input_buffer = []
        self.set_terminator("\n")
        self.socket_lock = allocate_lock()
    
    def thread_safe_push(self, data):
        with self.socket_lock:
            self.push(data)
            
    def handle_error(self):
        self.logger.error("================ ERROR! Failed to send something! ================ ")
        
    def handle_connect(self):
        # Init all the servos
        self.servoController = ServoController(self)
        
        self.logger.info("Sending CREEPER_READY status")
        self.push("CREEPER_READY:\n")
        
        
    def collect_incoming_data(self, data):
        self.input_buffer.append(data)
        
    def found_terminator(self):
        self.handle_android_command(self.input_buffer[0])
        self.input_buffer = []
        
    def handle_android_command(self, command_data):
        self.logger.info("Received command: %s" % command_data)
        self.servoController.process_command(command_data)

        



try:
    # Create socket and start the socket event loop 
    android_socket = AndroidSocket()
    asyncore.loop()
finally:
    print "Cleaning up..."
    try:
        android_socket.servoController.stop_all_servos()
    except AttributeError:
        pass
        
