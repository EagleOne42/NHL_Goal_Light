team = 'Blues' # Select the team you want normally

import datetime
import json
import os
import platform
import sys
import time
import socket


__author__ = 'EagleOne42'

i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/


def main():
	print 'Starting Main'
	print team

def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')

	
def print_help():
	print('By default games from yesterday and today will be displayed.')
	print('')
	print('If you want to see games from just today run the program with ')
	print('the "--today-only" flag.')


def parse_arguments(arguments):
	global show_today_only
	for x in range(1, len(arguments)):
		argument = arguments[x]
		
		if argument == '--help' or argument == '-h':
			print_help()
			sys.exit(0)
		elif argument == '--today-only':
			show_today_only = True
		elif argument == '-t' or argument == '--team':
			team = arguments[+2]
			print 'Your team is: %s' % team


if __name__ == '__main__':
	try:
		#Parse any arguments provided
		parse_arguments(sys.argv)

		# Start the main loop
		main()
		
	except KeyboardInterrupt:
		print 'Keyboard Interrupt'
		
	finally:
		print "Running GPIO Cleanup"

