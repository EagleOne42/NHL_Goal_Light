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
chan_list = [7,11,13,15,16]
GPIO.setup(chan_list, GPIO.OUT)


def main():
	clear_screen()
	
	print "Testing Lights"

	print "Testing flash_leds"
	flash_leds()

	print "Testing beacon_leds"
	beacon_leds()

	print "Testing lgb_leds"
	lgb_leds()


def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def beacon_leds():
	for i in range(0, 10):
		GPIO.output(7, True)
		time.sleep(0.1)
		GPIO.output(7, False)
		GPIO.output(11, True)
		time.sleep(0.1)
		GPIO.output(11, False)
		GPIO.output(15, True)
		time.sleep(0.1)
		GPIO.output(15, False)
		GPIO.output(16, True)
		time.sleep(0.1)
		GPIO.output(16, False)
		GPIO.output(13, True)
		time.sleep(0.1)
		GPIO.output(13, False)


def flash_leds():
	for i in range(0, 10):
		GPIO.output(chan_list, True) # Activate the light
		time.sleep(0.1)
		GPIO.output(chan_list, False) # Deactivate the light
		time.sleep(0.1)


def lgb_leds():
	print "LETS!"
	GPIO.output(chan_list, True) # Activate the light
	time.sleep(0.5)
	GPIO.output(chan_list, False) # Deactivate the light
	time.sleep(0.5)
	
	print "GO!"
	GPIO.output(chan_list, True) # Activate the light
	time.sleep(0.5)
	GPIO.output(chan_list, False) # Deactivate the light
	time.sleep(0.5)

	print "BLUES!!!" 
	GPIO.output(chan_list, True) # Activate the light
	time.sleep(1)
	GPIO.output(chan_list, False) # Deactivate the light
	print "Done - all off"
	time.sleep(1)


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

