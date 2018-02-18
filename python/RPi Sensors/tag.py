#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

# This is the default key for authentication
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		

def write_to_card(MIFAREReader,sector,data):
	if(len(data) != 9 or type(data) != list):
		raise "Invalid length or type of data",data
	
	# Scan for cards	
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# If a card is found
	if status == MIFAREReader.MI_OK:
		print "Card detected"
	
	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:

		# Print UID
		print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
	
		# Select the scanned tag
		MIFAREReader.MFRC522_SelectTag(uid)

		# Authenticate
		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, sector, key, uid)
		print "\n"

		# Check if authenticated
		if status == MIFAREReader.MI_OK:
			
			# Fill the rest of the data with 0xFF
			for x in range(0,7):
			   data.append(0xFF)

			print "Sector 8 looked like this:"
			# Read block 8
			MIFAREReader.MFRC522_Read(8)
			print "\n"

			print "Sector 8 will now be filled with the following data:"
			print("Length: " + str(len(data)) + ": " + str(data))
			# Write the data
			MIFAREReader.MFRC522_Write(sector, data)
			print "\n"

			print "It now looks like this:"
			# Check to see if it was written
			MIFAREReader.MFRC522_Read(8)
			print "\n"

			# Stop
			MIFAREReader.MFRC522_StopCrypto1()
		else:
			print "Authentication error"
			

def is_authorized_tag(MIFAREReader,authCode):
	print "Entered is_authorized_tag"
	read = True
	while read:
		# Scan for cards	
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		# If a card is found
		if status == MIFAREReader.MI_OK:
			print "Card detected"
		
		# Get the UID of the card
		(status,uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:

			# Print UID
			print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
		
			# Select the scanned tag
			MIFAREReader.MFRC522_SelectTag(uid)

			# Authenticate
			status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

			# Check if authenticated
			if status == MIFAREReader.MI_OK:
				data = MIFAREReader.MFRC522_Read(8)
				MIFAREReader.MFRC522_StopCrypto1()
				if(data[:9] == authCode):
					print "Authorized tag"
					return True
				else:
					print "Unauthorized tag"
					return False
				
				