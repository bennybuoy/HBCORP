#!/usr/bin/python

import serial
import time
import logging
import sys
import time
import string 
from serial import SerialException

logging.basicConfig(filename='ORPapp.log',level=logging.DEBUG)

def read_line():
	"""
	taken from the ftdi library and modified to 
	use the ezo line separator "\r"
	"""
	lsl = len('\r')
	line_buffer = []
	while True:
		next_char = ser.read(1)
		if next_char == '':
			break
		line_buffer.append(next_char)
		if (len(line_buffer) >= lsl and
				line_buffer[-lsl:] == list('\r')):
			break
	return ''.join(line_buffer)
	
def read_lines():
	"""
	also taken from ftdi lib to work with modified readline function
	"""
	lines = []
	try:
		while True:
			line = read_line()
			if not line:
				break
				ser.flush_input()
			lines.append(line)
		return lines
	
	except SerialException as e:
		print "Error, ", e
		return None	

def send_cmd(cmd):
	"""
	Send command to the Atlas Sensor.
	Before sending, add Carriage Return at the end of the command.
	:param cmd:
	:return:
	"""
	buf = cmd + "\r"     	# add carriage return
	try:
		ser.write(buf)
		return True
	except SerialException as e:
		print "Error, ", e
		logging.error(time.strftime("%c") + e)
		return None
			
if __name__ == "__main__":
	logging.info(time.strftime("%c")+ 'Main app started ')
	print "\nHBC ORP Logger\n"
	
	# to get a list of ports use the command: 
	# python -m serial.tools.list_ports
	# in the terminal
	usbport = '/dev/serial0' # change to match your pi's setup 

	print "Opening serial port now..."

	try:
		ser = serial.Serial(usbport, 9600, timeout=0)
	except serial.SerialException as e:
		logging.error(time.strftime("%c") + str(e))
		print "Error, ", e
		logging.info(time.strftime("%c") + ' Exiting')
		sys.exit(0)

	while True:
			delaytime = 1
	
			send_cmd("C,0") # turn off continuous mode
			#clear all previous data
			time.sleep(1)
			ser.flush()
			
			# get the information of the board you're polling
			#print("Polling sensor every 1 seconds, press ctrl-c to stop polling" % delaytime)
	
			try:
				while True:
					send_cmd("R")
					lines = read_lines()
					for i in range(len(lines)):
						print lines[i]
						logging.info(time.strftime("%c") + 'ORP Reading ' + str(i))
						if lines[i][0] != '*':
							print "Response: " , lines[i]
					time.sleep(delaytime)

			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")
	
		# if not a special keyword, pass commands straight to board
