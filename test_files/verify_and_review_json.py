import json
import os
import time

def main():
	global old_game_data
	print '--------------------'
	print 'Starting Main'

	for filename in sorted(os.listdir(os.getcwd())):
		print filename
		file_contents = open(filename, 'r').read()
		# Remove the leading JS
		file_contents = file_contents.replace('GCSB.load(', '')
		# Remove the trailing ')'
		json_data_game  = file_contents[:-1]

		#data_game = json.loads(json_data_game)
		data_game = parse_json(filename, json_data_game)

		h_dict = data_game['h']
		a_dict = data_game['a']

		home_team_score = h_dict['tot']['g']
		home_team_abv = h_dict['ab']
		print('Home - %s : %s' % (home_team_abv, home_team_score))
		away_team_score = a_dict['tot']['g']
		away_team_abv = a_dict['ab']
		print 'Away - %s : %s' % (away_team_abv, away_team_score)
		old_game_data = data_game


def parse_json(fname, json_input):
    try:
        return json.loads(json_input)
    except ValueError as e:
	print 'Using last file - Bad JSON data in file: ', fname
        print('invalid json: %s' % e)
	time.sleep(1)
        return old_game_data


if __name__ == '__main__':
	try:
		# Start the main loop
		main()
		
	except KeyboardInterrupt:
		print 'Keyboard Interrupt'
		
	finally:
		print "Done"

