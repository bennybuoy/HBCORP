#!/usr/bin/python

import serial
import time
import logging
import sys
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

def exitprog():
	logging.info(time.strftime("%c") + ' Exiting ')
	sys.exit(0)

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
		exitprog()

	while True:
		delaytime = 1
		# turn off continuous mode
		logging.info(time.strftime("%c")+ ' Turning off Continuous Logging')
		send_cmd("C,0")
		time.sleep(1)
		lines = read_lines()
		print lines[0]
		logging.info(time.strftime("%c") + ' Response - ' + lines[0])
		# clear all previous data
		ser.flush()
		print "Waiting 5 seconds to begin logging"
		#time.sleep(5)
		with open("log.csv", "a") as log:
			while True:
				try:
					while True:
						lines = []
						print 'Before read'
						print len(lines)
						send_cmd("R")
						time.sleep(delaytime)
						lines = read_lines()
						print 'After Read'
						print len(lines)
						print (lines[1] + ' ' + lines[2])
						logging.info(time.strftime("%c") + ' ORP Reading ' + lines[1] + ',' + lines[2])
						log.write("{0},{1},{2}\n".format(time.strftime("%c")),lines[1],lines[2])								
				except KeyboardInterrupt:
					exitprog()