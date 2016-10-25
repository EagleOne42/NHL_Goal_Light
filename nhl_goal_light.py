team = 'Blues' #Set default team

#Main team list
team_list = ('Avalanche', 'Blackhawks', 'Blue Jackets', 'Blues', 'Bruins', 'Canadiens', 'Canucks', 'Capitals', 'Coyotes', 'Devils', 'Ducks', 'Flames', 'Flyers', 'Hurricanes', 'Islanders', 'Jets', 'Kings', 'Lightning', 'Maple Leafs', 'Oilers', 'Panthers', 'Penguins', 'Predators', 'Rangers', 'Red Wings', 'Sabres', 'Senators', 'Sharks', 'Stars', 'Wild')

#List of alternate names for teams
nhl_team_dict = {
	'Anaheim': 'Ducks',
	'ANA': 'Ducks',
	'Arizona': 'Coyototes',
	'Phoenix': 'Coyototes',
	'ARI': 'Coyotes',
	'Boston': 'Bruins',
	'BOS': 'Bruins',
	'Buffalo': 'Sabres',
	'BUF': 'Sabres',
	'Carolina': 'Hurricanes',
	'CAR': 'Hurricanes',
	'Columbus': 'Blue Jackets',
	'Jackets': 'Blue Jackets',
	'CBJ': 'Blue Jackets',
	'Calgary': 'Flames',
	'CGY': 'Flames',
	'Chicago': 'Blackhawks',
	'Black Hawks': 'Blackhawks',
	'CHI': 'Blackhawks',
	'Colorado': 'Avalanche',
	'Avs': 'Avalanche',
	'COL': 'Avalanche',
	'Dallas': 'Stars',
	'DAL': 'Stars',
	'Detroit': 'Red Wings',
	'Wings': 'Red Wings',
	'Redwings': 'Red Wings',
	'DET': 'Red Wings',
	'Edmonton': 'Oilers',
	'EDM': 'Oilers',
	'Florida': 'Panthers',
	'FLA': 'Panthers',
	'Los Angeles': 'Kings',
	'LAK': 'Kings',
	'Minnesota': 'Wild',
	'MIN': 'Wild',
	'Montreal': 'Canadiens',
	'MTL': 'Canadiens',
	'New Jersey': 'Devils',
	'NJD': 'Devils',
	'Nashville': 'Predators',
	'Perds': 'Predators',
	'NSH': 'Predators',
	'NYI': 'Islanders',
	'NYR': 'Rangers',
	'Ottawa': 'Senators',
	'OTT': 'Senators',
	'Philadelphia': 'Flyers',
	'PHI': 'Flyers',
	'Pittsburgh': 'Penguins',
	'PIT': 'Penguins',
	'San Jose': 'Sharks',
	'SJS': 'Sharks',
	'St Louis': 'Blues',
	'St. Louis': 'Blues',
	'Saint Louis': 'Blues',
	'STL': 'Blues',
	'Tampa Bay': 'Lightning',
	'TBL': 'Lightning',
	'Toronto': 'Maple Leafs',
	'Leafs': 'Maple Leafs',
	'TOR': 'Maple Leafs',
	'Vancouver': 'Canucks',
	'VAN': 'Canucks',
	'Winnipeg': 'Jets',
	'WPG': 'Jets',
	'Washington': 'Captials',
	'Caps': 'Captials',
	'WSH': 'Capitals'
}

from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests
import getopt
import socket
print('Disabled GPIO')#gpio_disable try:
print('Disabled GPIO')#gpio_disable 	import RPi.GPIO as GPIO
print('Disabled GPIO')#gpio_disable except RuntimeError:
print('Disabled GPIO')#gpio_disable 	print ("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

print('Disabled GPIO')#gpio_disable GPIO.setmode(GPIO.BOARD) #Use the pin number, not the GPIO name - example use "7" for pin #7 aka GPIO4
print('Disabled GPIO')#gpio_disable goal_light_gpio_pins = [7] #For multiple lights enter the gpio like this - [7,11,13,15,16]
print('Disabled GPIO')#gpio_disable GPIO.setup(goal_light_gpio_pins, GPIO.OUT) #Set the Raspberry Pi GPIO pins as output to activate relays/leds

target = open('logs/goal_log.txt', 'a')
target.write('Script startup at %s\n' % str(datetime.datetime.now()))
target.close()

refresh_time = 21600  # 6 hours Refresh time (seconds), NHL API refresh is every 60 seconds
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp' #NHL JSON API with the game IDs and basic info
#'game_api_url' is defined in the code below to pull the score for each game - should update more often then the 'api_url'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

#Home team variables
home_old_score = 0
team_playing = False

#Away team variables
away_old_score = 0
show_today_only = False


def main():
	global refresh_time
	global team
	global team_playing
	global home_old_score
	global away_old_score
	global old_game_data
	clear_screen()
	
	# Format dates to match NHL API style:
	# Todays date
	t = datetime.datetime.now()
	todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
	
	# Yesterdays date
	y =y = t - datetime.timedelta(days=1)
	yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)
	
	while True:
		try:
			scoreboard_jsonp_web = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
		except (requests.ConnectionError): #Catch these errors
			print ("Could not get response from NHL.com trying again...")
			time.sleep(5)
			continue
		except(requests.HTTPError):
			print ("HTTP Error when loading url. Please restart program. ")
			sys.exit(0)
		except(requests.Timeout):
			print ("The request took too long to process and timed out. Trying again... ")
			time.sleep(5)
		except(socket.error):
			print ("Could not get response from NHL.com trying again...")
			time.sleep(5)
		except(requests.RequestException):
			print ("Unknown error. Please restart the program. ")
			sys.exit(0)
			
		# We get back JSON data with some JS around it, gotta remove the JS
		scoreboard_jsonp_data = scoreboard_jsonp_web.text
		# Remove the leading JS
		scoreboard_json_data = scoreboard_jsonp_data.replace('loadScoreboard(', '')
		# Remove the trailing ')'
		scoreboard_json_data  = scoreboard_json_data[:-1]
		#Send to the parse function and save the cleaned json data
		scoreboard_json_data_clean = parse_json(scoreboard_json_data)
		
		print ("Start json parse")
		for key in scoreboard_json_data_clean:
			if key == 'games':
				for game_info in scoreboard_json_data_clean[key]:
					print ("Away team is %s " % game_info['atv'].title())
					print ("Home team is %s " % game_info['htv'].title())
					if ( game_info['atv'].title() == team ) or ( game_info['htv'].title() == team ):
						# Assign more meaningful names
						gc_id = game_info['id']
						print ("Game ID: %d " % gc_id)
						game_clock = game_info['ts']
						game_stage = game_info['tsc']
						status = game_info['bs']
						
						away_team_locale = game_info['atn']
						away_team_name = game_info['atv'].title()
						away_team_result = game_info['atc']
						
						home_team_locale = game_info['htn']
						home_team_name = game_info['htv'].title()
						home_team_result = game_info['htc']
						
						# Fix strange names / locales returned by NHL
						away_team_locale = fix_locale(away_team_locale)
						home_team_locale = fix_locale(home_team_locale)
						away_team_name = fix_name(away_team_name)
						home_team_name = fix_name(home_team_name)
						
						game_api_url = 'http://live.nhle.com/GameData/20162017/%d/gc/gcsb.jsonp' % gc_id
		print ("End of main. ")


def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def print_help():
	print('Help:')
	print('By default games from yesterday and today will be displayed.')
	print('If you want to see games from just today run the program with ')
	print('the "--today-only" flag.')
	print('')
	print('Teams can be specified by the \'-t\' or \'--team\'')
	print('Example:')
	print('python Scoreboard.py -t \'Maple Leafs\'')


def fix_locale(team_locale):
	# NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
	if 'NY ' in team_locale:
		return 'New York'
	
	if 'Montr' in team_locale:
		return 'Montreal'
	
	return team_locale


def fix_name(team_name):
	#Change 'redwings' to 'Red Wings'
	if 'wings' in team_name:
		return 'Red Wings'
	
	if 'jackets' in team_name:
		return 'Blue Jackets'
	
	if 'leafs' in team_name:
		return 'Maple Leafs'
	
	return team_name


def setup_light():
	light_on()
	print "1) Steady On"
	print "2) 3 Flashes - 1, then 2"
	print "3) 1 Flash"
	print "4) Rotating Beacon (Goal Light)"
	print ''
	starting_mode = int(input("Enter 1-4 for the current mode "))
	print 'You entered:', starting_mode
	light_off()
	
	if starting_mode == 1:
		for i in range(0, 2):
			cycle_light()
		print 'Light ready'
	elif starting_mode == 2:
		for i in range(1, 2):
			cycle_light()
		print 'Light ready'
	elif starting_mode == 3:
		light_off()
		print 'Light ready'
	elif starting_mode == 4:
		print 'Testing Reset Light'
		reset_light()
		print 'Light ready'
	else:
		print('Invalid choice!')
		setup_light()
		return
		
	light_on()
	raw_input("Press Enter to continue if the light in is beacon (rotating) mode - if not, restart this script...")
	light_off()	
	reset_light()


def reset_light():
	for i in range(1, 4):
		cycle_light()


def light_on():
	print('Disabled GPIO')#gpio_disable GPIO.output(goal_light_gpio_pins, True)
	print('Disabled GPIO')#gpio_disable time.sleep(0.25)


def light_off():
	print('Disabled GPIO')#gpio_disable GPIO.output(goal_light_gpio_pins, False)
	time.sleep(0.25)
		


def cycle_light():
	light_on()
	light_off()


def activate_goal_light():
	print 'Activating Goal light'
	print('Disabled GPIO')#gpio_disable light_on()
	print('Disabled GPIO')#gpio_disable time.sleep(10) #Leave light on for 10 secs - GOAL!!!
	print('Disabled GPIO')#gpio_disable light_off()
	print('Disabled GPIO')#gpio_disable reset_light()


def parse_arguments(argv):
	try:
		opts, args = getopt.getopt(argv, "ht:d", ["help", "team=", "today-only"])
	except getopt.GetoptError:
		print ''
		print 'Invalid option'
		print ''
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Help'
			print_help()
			sys.exit()
		elif opt in ("-d", "--today-only"):
			global show_today_only
			show_today_only = True
		elif opt in ("-t", "--team"):
			global team
			if arg in team_list:
				team = arg
			else:
				try:
					team = nhl_team_dict[arg]
				except:
					print 'Team name not in list.  Make sure to use single quote around name.'
					print 'You can use team name, city/location, or the 3 letter name used by the NHL'
					print "Example) For the St. Louis Blues you can use 'Blues' or 'St Louis' or 'St. Louis' or 'STL'"
					print 'List of teams: %s' % (team_list,)
					sys.exit()


def parse_json(json_input):
	try:
		return json.loads(json_input)
	except ValueError as e:
		print 'Using last file - Bad JSON data'
		print('invalid json: %s' % e)
		time.sleep(1)
		return old_game_data


if __name__ == '__main__':
	try:
		# Initialize Colorama
		init()
		
		# Parse any arguments provided
		parse_arguments(sys.argv[1:])
		
		# Run the setup light
		setup_light()
		
		# Start the main loop
		main()
	
	except KeyboardInterrupt:
		print 'Keyboard Interrupt'
	
	finally:
		print "Running GPIO Cleanup"
		print('Disabled GPIO')#gpio_disable GPIO.cleanup() # this ensures a clean exit

