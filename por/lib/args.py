# parses command line for arguments
# http://bit.ly/x1b5DS

from getopt import getopt
from sys import argv, exit

def getArgs():
	opts = 'd:h'
	words = ['help']
	args = dict({
		'directory' : ''})

	# get command line arguments
	try:
		options, params = getopt(argv[1:], opts, words)
	except GetoptError, err:
		error(str(err))

	# set variables
	for option, param in options:
		if(option in ('-h', '--help')):
			usage()
			exit(0)
		elif(option == '-d'):
			args['directory'] = str(param)

	if(args['directory'] == ''):
		usage()
		exit()
	return(args)

def usage():
	print(('usage: %s ( -h | --help | -d (string))') % argv[0])
	print((' -d(irectory) : directory of all the threads'))
