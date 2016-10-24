import json
import os
import time

def main():
	print '----------------------------------------------------------------------------'
	print 'Verifing files in current folder for valid JSON'
	print '----------------------------------------------------------------------------'

	open('files_with_invalid_json.txt', 'w').close()

	for filename in sorted(os.listdir(os.getcwd())):
		file_contents = open(filename, 'r').read()
		# Remove the leading JS
		file_contents = file_contents.replace('GCSB.load(', '')
		# Remove the trailing ')'
		json_data_game  = file_contents[:-1]

		data_game = parse_json(filename, json_data_game)

	print '----------------------------------------------------------------------------'
	print 'Completed - file list saved to files_with_invalid_json.txt'
	print '----------------------------------------------------------------------------'


def parse_json(fname, json_input):
    try:
        return json.loads(json_input)
    except ValueError as e:
	print fname
        print('invalid json: %s' % e)
	target = open('files_with_invalid_json.txt', 'a')
	target.write('%s\n' % fname)
	target.close()
        return None


if __name__ == '__main__':
	try:
		# Start the main loop
		main()
		
	except KeyboardInterrupt:
		print 'Keyboard Interrupt'
		
	finally:
		print "Done"

