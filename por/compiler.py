from os import listdir
from sys import exit
from lib.args import getArgs

def main():
	args = getArgs()
	try:
		listdir(args['directory'])
	except OSError, err:
		print(err)
		exit()

	# directory listing of all files in the given directory
	dl = listdir(args['directory'])

	files = dict()
	# processes for only thread files (*.thread)
	for file in dl:
		(name, extension) = file.split('.')
		if(extension == 'thread'):
			(block, order) = (name.split('_'))
			if(block in files):
				files[block].append(order)
			else:
				files[block] = [order]

	# sort files
	for block in files:
		files[block] = sorted(files[block])

	# inits the handler daemon
	code = [
		'from multiprocessing import Process, Pipe, Manager, Queue',
		'from classes.proc import Proc',
		'from scripts.handler import handler',
		'queue = Queue()',
		'handler = Proc(\'handler\', handler, {\'queue\' : queue, \'globals\' : Manager().dict()})',
		'handler.daemon = True',
		'handler.start()']

	# inits the process list
	processCode = list()
	for block in files:
		processCode.append(blockProc(args['directory'], block, files[block]))
	for block in files:
		processCode.append('proc%s.start()' % block)
	code.append('processes = Proc(\'processes\', %s, {\'queue\' : queue})' % format('\n'.join(processCode)))
	code.append('processes.start()')
	code.append('processes.join()')

	# waits for processes to finish, then terminates code
	code += [
		'queue.put(None)',
		'handler.join()']

	print('\n'.join(code))

# generates a list of processes that must be run sequentially (within the block process)
def blockProc(dirName, blockName, orderNames):
	code = list()
	for order in orderNames:
		filename = (('%s/%s_%s.thread') % (dirName, blockName, order))
		fp = open(filename, 'r')
		instructions = fp.read()
		fp.close()
		code.append('proc%s = Proc(\'%s_%s\', %s, {\'queue\' : self.var[\'queue\']})' % (order, blockName, order, format(instructions)))
		code.append('proc%s.start()' % order)
		code.append('proc%s.join()' % order)
	instructions = "\n".join(code)
	return('proc%s = Proc(\'%s\', %s, {\'queue\' : self.var[\'queue\']})' % (blockName, blockName, format('\n%s\n' % instructions)))

# wraps the instructions in a deeper level of quotes
def format(instr):
	return(('"""%s"""') % (instr.replace('\"', '\\\"').replace('"', '\"')))

main()
