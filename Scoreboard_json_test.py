team_list = ('Avalanche', 'Blackhawks', 'Blue Jackets', 'Blues', 'Bruins', 'Canadiens', 'Canucks', 'Capitals', 'Coyotes', 'Devils', 'Ducks', 'Flames', 'Flyers', 'Hurricanes', 'Islanders', 'Jets', 'Kings', 'Lightning', 'Maple Leafs', 'Oilers', 'Panthers', 'Penguins', 'Predators', 'Rangers', 'Red Wings', 'Sabres', 'Senators', 'Sharks', 'Stars', 'Wild')

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
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print ("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

GPIO.setmode(GPIO.BOARD) #Use the pin number, not the GPIO name - example use "7" for pin #7 aka GPIO4
goal_light_gpio_pins = [7]
GPIO.setup(goal_light_gpio_pins, GPIO.OUT) #Set the Raspberry Pi GPIO pin 7 as output to activate relay

refresh_time = 5  # 6 hours Refresh time (seconds), NHL API refresh is every 60 seconds
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp' #NHL JSON API with the game IDs and basic info
#'game_api_url' is defined in the code below to pull the score for each game
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

#Home team variables
old_score = 0
team_playing = False

#Away team variables
away_old_score = 0
show_today_only = False


def main():
	global refresh_time
	global team
	global team_playing
	global old_score
	global away_old_score
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
				r = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
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
			json_data = r.text
			
			# Remove the leading JS
			json_data = json_data.replace('loadScoreboard(', '')
			
			# Remove the trailing ')'
			json_data  = json_data[:-1]
			
			data = json.loads(json_data)
			for key in data:
				if key == 'games':
					for game_info in data[key]:
					
						# Assign more meaningful names
						gc_id = game_info['id']
						game_clock = game_info['ts']
						game_stage = game_info['tsc']
						status = game_info['bs']
						
						away_team_locale = game_info['atn']
						away_team_name = game_info['atv'].title()
						#away_team_score = game_info['ats']
						away_team_result = game_info['atc']
						
						
						home_team_locale = game_info['htn']
						home_team_name = game_info['htv'].title()
						#home_team_score = game_info['hts']
						home_team_result = game_info['htc']
						
						# Fix strange names / locales returned by NHL
						away_team_locale = fix_locale(away_team_locale)
						home_team_locale = fix_locale(home_team_locale)
						away_team_name = fix_name(away_team_name)
						home_team_name = fix_name(home_team_name)
						
						game_api_url = 'http://live.nhle.com/GameData/20152016/%d/gc/gcsb.jsonp' % gc_id
						
						try:
							q = requests.get(game_api_url, headers=api_headers) #making sure there is a connection with the API
						except(requests.ConnectionError): #Catch these errors
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
						json_data_game = q.text
						
						# Remove the leading JS
						json_data_game = json_data_game.replace('GCSB.load(', '')
						
						# Remove the trailing ')'
						json_data_game  = json_data_game[:-1]
						
						data_game = json.loads(json_data_game)
						
						h_dict = data_game['h']
						a_dict = data_game['a']
						
						home_team_score = h_dict['tot']['g']
						away_team_score = a_dict['tot']['g']
						
						
						# Show games from Yesterday and today or just today
						if (yesterdays_date in game_clock.title() and not show_today_only) or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:
						
							header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
							
							# Different displays for different states of game:
							# Game from yesterday, ex: on YESTERDAY, MONDAY 4/20 (FINAL 2nd OT)
							# Game from today finished, ex: TODAY (FINAL 2nd OT)
							if 'FINAL' in status:
								if yesterdays_date in game_clock.title():
									header_text += '\nYESTERDAY, ' + game_clock + ' '
								elif todays_date in game_clock.title() or 'TODAY' in game_clock:
									header_text += '\nTODAY '
								header_text += '(' + status + ')'
								
							# Upcoming game, ex: TUESDAY 4/21, 7:00 PM EST)
							elif 'DAY' in game_clock:
								header_text += Fore.YELLOW + '\n(' + game_clock + ', ' + status + ' EST)' + Fore.RESET
							
							# Last 5 minutes of game and overtime, ex: (1:59 3rd PERIOD) *in red font*
							elif 'critical' in game_stage:
								header_text += '\n(' + Fore.RED + game_clock + ' PERIOD' + Fore.RESET + ')'
							
							
							# Any other time in game, ex: (10:34 1st PERIOD)
							else:
								header_text += Fore.YELLOW + '\n(' + game_clock + ' PERIOD)' + Style.RESET_ALL
							
							
							print(header_text)
							
							
							
							
							
							# Highlight the winner of finished games in green, and games underway in blue:
							# Away team wins
							if away_team_result == 'winner':
								#print(Style.BRIGHT + Fore.GREEN + away_team_name + ': ' + away_team_score + Style.RESET_ALL)
								print(Style.BRIGHT + Fore.GREEN + away_team_name + ': ' + str(away_team_score) + Style.RESET_ALL)
								print(home_team_name + ': ' + str(home_team_score))
							
							
							# Home team wins
							elif home_team_result == 'winner':
								print(away_team_name + ': ' + str(away_team_score))
								print(Style.BRIGHT + Fore.GREEN + home_team_name + ': ' + str(home_team_score) + Style.RESET_ALL)
							
							# Game still underway
							elif 'progress' in game_stage or 'critical' in game_stage:
								print(Fore.CYAN + away_team_name + ': ' + str(away_team_score))
								print(home_team_name + ': ' + str(home_team_score) + Fore.RESET)
								game_current(home_team_name,home_team_score,game_clock,status) 
								game_current(away_team_name,away_team_score,game_clock,status)
								
							# Game hasn't yet started
							else:
								print(away_team_name + ': ' + str(away_team_score))
								print(home_team_name + ': ' + str(home_team_score))
								game_current(home_team_name,home_team_score,game_clock,status)
								game_current(away_team_name,away_team_score,game_clock,status)
							print('')
							if ('FINAL' in status) and (away_team_name == team or home_team_name == team) and (yesterdays_date in game_clock.title() or todays_date in game_clock.title() ): #Game over, no need to refresh every minute
								print "Game over!"
								refresh_time = 5
								team_playing = False
								old_score = 0 
								away_old_score = 0
								print "Refresh in: " + str(refresh_time) + " seconds (6 hours)"
								print "Team playing: " + str(team_playing)
								print ""
								
			if team_playing == False:
				print ("Current time: " + str(datetime.datetime.now()))
				refresh_time = 5 # 6 hours
				print team + " are not playing. Refreshing in " + str(refresh_time) + " seconds (6 hours)."
			# Perfrom the refresh
			time.sleep(refresh_time)


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


def game_current(current_team_name, current_team_score, game_clock, status):
	global refresh_time
	global old_score
	global team_playing
	current_time = time.strftime("%I:%M:%S")
	game_time = str(status)
	game_date = game_clock
	now = datetime.datetime.now()
	now_second = now.second	
	
	if team in current_team_name:
		print""
		print""
		print ("Current time: " + current_time) 
		team_playing = True
		
		if (game_date != "TODAY" and game_time != "LIVE"):
			print("Game time is quite aways away!")
			refresh_time = 5 # 6 hours
			old_score = 0
			print "Refreh time: " + str(refresh_time) + " seconds (6 hours)"
			print "Current old_score: " + str(old_score)
		
		
		elif (game_date == "TODAY"): #Game time is near
			refresh_time = 3600 # 1 hours
			print "It is game day!"
			print "Refresh time is : " + str(refresh_time) + " seconds (1 hour)"
		
		
		elif (game_date == "PRE GAME"): #30 minutes to game time
			refresh_time = 300 # 5 minutes
			print "It is almost game time!"
			print "Refresh time: " + str(refresh_time) + " seconds (5 minutes)"
		
		
		else: # Game is underway
			print "Now: " + str(now)
			print "Now.second: " + str(now_second)
			
			#The API url refreshes at exactly the next minute. So we calculate the time until the next minute, set it to refresh then
			#refresh_time = 63 - now.second - now.microsecond/1e6
			refresh_time = 10
			print "Time untill next minute: " + str(refresh_time)
			print "Refresh time: " + str(refresh_time) + " seconds"
			print "Current old_score: " + str(old_score)
			
			
			if int(old_score) < int(current_team_score): # If the old score < the new score, a goal was scored
				print team + " have scored a goal!"
				time.sleep(20) #enter delay here
				activate_goal_light()
				old_score = int(current_team_score) # Set the old_score to be the current score
				print "Current old_score: " + str(old_score)
				
	elif team_playing == False: # The selected team isn't playing
		refresh_time = 5 # 6 hours
		old_score = 0
		print "Current old_score: " + str(old_score)
		print "Not " + team + " gameday!! Refresh in: " + str(refresh_time) + " seconds (6 hours)"


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
		
	print 'TEST GOAL LIGHT!!! - The light should be in beacon (rotating) mode - if not, restart this script'
	activate_goal_light()


def reset_light():
	for i in range(0, 3):
		cycle_light()

def light_on():
	GPIO.output(goal_light_gpio_pins, True)
	time.sleep(0.25)


def light_off():
	GPIO.output(goal_light_gpio_pins, False)
	time.sleep(0.25)
		

def cycle_light():
	light_on()
	light_off()


def activate_goal_light():
	print 'Activating Goal light'
	light_on()
	time.sleep(10) #Leave light on for 10 secs - GOAL!!!
	light_off()
	reset_light()


def parse_arguments(argv):
	try:                                
        	opts, args = getopt.getopt(argv, "ht:d", ["help", "team=", "today-only"])
    	except getopt.GetoptError:          
		print 'Error'                         
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
				print 'Team name not in list.  Make sure to use single quote around name.'
				print 'List of teams: %s' % (team_list,)
				sys.exit()


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
		GPIO.cleanup() # this ensures a clean exit

