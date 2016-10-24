team = 'Blues' # Select the team you want normally

team_list = ('Avalanche', 'Blackhawks', 'Blue Jackets', 'Blues', 'Bruins', 'Canadiens', 'Canucks', 'Capitals', 'Coyotes', 'Devils', 'Ducks', 'Flames', 'Flyers', 'Hurricanes', 'Islanders', 'Jets', 'Kings', 'Lightning', 'Maple Leafs', 'Oilers', 'Panthers', 'Penguins', 'Predators', 'Rangers', 'Red Wings', 'Sabres', 'Senators', 'Sharks', 'Stars', 'Wild')

import datetime
import json
import os
import platform
import sys
import time
import socket
import getopt
import requests

__author__ = 'EagleOne42'

i = datetime.datetime.now()  # date and time formatting http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

show_today_only = False
nhl_year='20152016'
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

#Home team variables
old_score = 0
team_playing = False

#Away team variables
away_old_score = 0

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


def main():
	print '--------------------'
	print 'Starting Main'
	print 'Only Show today\'s games: %s' % show_today_only
	print 'Team is: %s' % team
	time.sleep(2)
	
	while True:
			try:
				scoreboard_request = requests.get(api_url, headers=api_headers) #making sure there is a connection with the API
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
			scoreboard_json_data = scoreboard_request.text
			
			# Remove the leading JS
			scoreboard_json_data = scoreboard_json_data.replace('loadScoreboard(', '')
			
			# Remove the trailing ')'
			scoreboard_json_data  = scoreboard_json_data[:-1]
			
			scoreboard_data = json.loads(scoreboard_json_data)
			for key in scoreboard_data:
				if key == 'games':
					for game_info in scoreboard_data[key]:
					
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

						print('')
						print('Game ID: %d' % gc_id)
						home_team_score = h_dict['tot']['g']
						home_team_abv = h_dict['ab']
						print('Home - %s : %s' % (home_team_abv, home_team_score))
						away_team_score = a_dict['tot']['g']
						away_team_abv = a_dict['ab']
						print 'Away - %s : %s' % (away_team_abv, away_team_score)

			print 'Sleeping...'
			time.sleep(10)


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


def clear_screen():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')

	
def print_help():
#	print('By default games from yesterday and today will be displayed.')
#	print('If you want to see games from just today run the program with ')
#	print('the "--today-only" flag.')
#	print('')
	print('Teams can be specified by the \'-t\' or \'--team\'')
	print('Example:')
	print('python Scoreboard.py -t \'Maple Leafs\'')
	print 'You can use team name, city/location, or the 3 letter name used by the NHL'
	print "Example) For the St. Louis Blues you can use 'Blues' or 'St Louis' or 'St. Louis' or 'STL'"


def set_arguments(argv):
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


if __name__ == '__main__':
	try:
		#Parse any arguments provided
		#parse_arguments(sys.argv)
		set_arguments(sys.argv[1:])
		
		# Start the main loop
		main()
		
	except KeyboardInterrupt:
		print 'Keyboard Interrupt'
		
	finally:
		print "Running GPIO Cleanup"

