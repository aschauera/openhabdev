#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import lcddriver
import display
import tag
import sys
import openhab
import time
import matrix_keypad

continue_reading = True
inMainMenu = True
authenticated = False
#Create keypad
kp = matrix_keypad.keypad(columnCount = 3)

##########################################################################################
# Provides interactive LED display menu and read functions for Mifare Tags and functions #
# for OPENHAB alarm system activation/deactivation										 #
##########################################################################################

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	global inMainMenu
	global authenticated
	display.set_line_1("Alarm system",1,True)
	display.set_line_2("# STOPPED #",2,False)
	print "Ctrl+C captured, cleaning up.."
	continue_reading = False
	GPIO.cleanup()

def digit():
    GPIO.setmode(GPIO.BCM)
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

#This is the "house code" - tags need to be initied with this code to be authorized
authCode = [1,2,0,3,99,1,2,0,3]
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
# Create display
display = display.Display()

# Welcome message
display.print_welcome_screen()


print "Entering main menu"
##################################
# Interactive main menu display	 #
##################################
try:
	while continue_reading:
		authenticated = tag.is_authorized_tag(MIFAREReader, authCode)
		if(authenticated):
			while inMainMenu:
				display.set_line_1("Main Menu",clear=True)
				display.set_line_2("1=Write,2=Start")
				authenticated=True
				 # Loop while waiting for a keypress
				value = digit()
     
				if value==1:
					display.set_line_1("# Auth new tag #")
					#Write "house code" to make this an authorized tag
					tag.write_to_card(MIFAREReader, 8, authCode)
				
				elif value==2:
					display.set_line_1("# INACTIVE #",clear=True)
					display.set_line_2(">>Activate alarm")
					# todo loop
					# Scan for cards	
					authenticated = tag.is_authorized_tag(MIFAREReader,authCode)
					if authenticated:
						openhab.activate_alarm()
					else:
						display.set_line_1("Unauthorized",1,True)
						display.set_line_2(">> Try again")
						time.sleep(3)
				else:
					break;
		else:
			authenticated=False
			display.set_line_1("Unauthorized")
			display.set_line_2(">> Try again")
			time.sleep(3)
						
					
except Exception,e:
	display.print_to_display("# System Error #",1)
	print e
finally:
	GPIO.cleanup()

