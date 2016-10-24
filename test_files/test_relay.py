from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests
import RPi.GPIO as GPIO
import socket 

i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)


def main():
	clear_screen()
	
	setup_lights()
	
	print 'GOAL!!!'
	GPIO.output(7, True)
	time.sleep(5)
	GPIO.output(7, False)
	time.sleep(0.2)
	
	print "Off"


def setup_lights():
	GPIO.output(7, True)
	print "1) Steady On"
	print "2) 3 Flashes - 1, then 2"
	print "3) 1 Flash"
	print "4) Rotating Beacon (Goal Light)"
	starting_mode = int(input("Enter 1-4 for the current mode"))
	print 'You entered:', starting_mode
	GPIO.output(7, False)
	time.sleep(0.2)
	
	if starting_mode == 1:
		for i in range(0, 2):
			cycle_light()
		print 'Light ready'
	elif starting_mode == 2:
		for i in range(1, 2):
			cycle_light()
		print 'Light ready'
	elif starting_mode == 3:
		GPIO.output(7, False)
		time.sleep(0.2)
		print 'Light ready'
	elif starting_mode == 4:
		print 'Testing Reset Light'
		reset_light()
		print 'Light ready'
	
def reset_light():
	for i in range(0, 3):
		cycle_light()
		

def cycle_light():
	GPIO.output(7, True)
	time.sleep(0.2)
	GPIO.output(7, False)
	time.sleep(0.2)


def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


if __name__ == '__main__':
	try:
		# Initialize Colorama
		init()

		# Start the main loop
		main()

	except KeyboardInterrupt:
		print 'Keyboard Interrupt'

	finally:
		print "Running GPIO Cleanup"
		GPIO.cleanup() # this ensures a clean exit

