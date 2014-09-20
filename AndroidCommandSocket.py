#!/usr/bin/python

import asynchat, asyncore, socket
import logging
import sys, traceback
from threading import RLock
from CommandDispatcher import CommandDispatcher

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

#ANDROID_HOST = ("192.168.7.101", 4444)
ANDROID_HOST = ("192.168.43.1", 4444)

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
        self.socket_lock = RLock()
    
    # Making async_chat thread-safe
    def push(self, data):
        try:
            self.socket_lock.acquire()
            asynchat.async_chat.push(self, data)
        finally:
            self.socket_lock.release()
    
    # Making async_chat thread-safe
    def initiate_send(self):
        try:
            self.socket_lock.acquire()
            asynchat.async_chat.initiate_send(self)
        finally:
            self.socket_lock.release()
        
            
    def handle_error(self):
        self.logger.error("================ ERROR! Failed to send something! ================ ")
        etype, value, tb = sys.exc_info()
        traceback.print_exception(etype, value, tb)
        
    def handle_connect(self):
        # Init all the devices we need to control
        try:
            self.commandDispatcher = CommandDispatcher(self)
        except Exception as e:
            print e
            raise e
        
        self.logger.info("Sending CREEPER_READY status")
        self.push("CREEPER_READY:\n")
        
        
    def collect_incoming_data(self, data):
        self.input_buffer.append(data)
        
    def found_terminator(self):
        self.handle_android_command(self.input_buffer[0])
        self.input_buffer = []
        
    def handle_android_command(self, command_data):
        self.logger.info("Received command: %s" % command_data)
        self.commandDispatcher.process_command(command_data)

        



try:
    # Create socket and start the socket event loop 
    android_socket = AndroidSocket()
    asyncore.loop()
finally:
    print "Cleaning up..."
    try:
        android_socket.commandDispatcher.stop_all_devices()
    except AttributeError:
        pass
        
