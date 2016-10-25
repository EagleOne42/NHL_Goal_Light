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

target = open('goal_log.txt', 'a')
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


