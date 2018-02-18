#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import lcddriver
from time import *

class Display:
	
	lcd=lcddriver.lcd()
	
	# Print to stdout and LCD clearing lines by default
	def print_to_display(self, text, line=1,clear=True):
		"Prints text to stdout and the LCD display"
		print(text)
		if(clear):
			self.lcd.lcd_clear()
		self.lcd.lcd_display_string(text,line)
	# Sets line 1 of the display keeping line 2 by default
	def set_line_1(self, text, line=1,clear=False):
		"Prints text to stdout and the LCD display"
		print(text)
		if(clear):
			self.lcd.lcd_clear()
		self.lcd.lcd_display_string(text,line)
	# Sets line 2 of the display keeping line 1 by default
	def set_line_2(self, text, line=2,clear=False):
		"Prints text to stdout and the LCD display"
		print(text)
		if(clear):
			self.lcd.lcd_clear()
		self.lcd.lcd_display_string(text,line)
	# Prints the welcome screen right after startup and waits for an authorized tag is swiped
	def print_welcome_screen(self):
		self.set_line_1("  # Welcome #")
		self.set_line_2(">> Authenticate")
	#Prints the main menu and options and waits for a tag or an input
	def print_main_menu(self):
		self.set_line_1("Main Menu",clear=True)
		self.set_line_2("1=Write,2=Start")
	

