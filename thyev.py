# this is a start - the basics of thread Object -> thread execution logic is developed here
# things to do - shared variable logic

# apparently Processes are a lot easier to implement than Threads in Unix environments
# http://bit.ly/d89oa8

from multiprocessing import Process
import random, time

# the process class
class Proc(Process):
	def __init__(self, id, instr = '', var = dict()):
		self.id = id
		# instructions to be run - note that instructions are all in 'one' line
		self.instr = str(instr)
		# list of variables in a dictionary form
		self.var = var
		Process.__init__(self)
	def run(self):
		# execute the instruction
		exec(self.instr)

# run a quick block of identical processes
def runBlock(instr, var, concurrent = True):
	print('\nprocessing new block')
	for id in xrange(10):
		# init 100 processes
		proc = Proc(id, instr, var)
		# each process is to print out a string after rand() seconds
		proc.start()
		# .join() enforces current proc to finish before iterating
		if(not(concurrent)):
			proc.join()

# wraps the instructions in a deeper level of quotes
def format(instr):
	return(('"""%s"""') % (instr.replace('"""', '\"\"\"')))


# examples

# instruction set - triple quotes mark entire block as single string
sleep = """
self.var['time'] = random.randint(0, 3)
time.sleep(self.var['time'])
# note that the instance variable is passed literally as if the instruction is sub'd into Proc.run()
# i.e. the liberal use of 'self' to refer to the process
print(('process %s slept for %s seconds') % (self.id, self.var['time']))
"""

# demonstrates the use of vars in each process
rand = """
print(('process %s with var %s') % (self.id, self.var['rand']))
"""

# ensure both processes are run after one another
sleep = Proc('sleep', (('runBlock(%s, {})') % (format(sleep))))
# note where the variable dictionary goes in this invocation
rand = Proc('random', (('runBlock(%s, {\'rand\' : random.random()}), False') % (format(rand))))

sleep.start()
sleep.join()
rand.start()
rand.join()

# data sharing - work in progress

# from multiprocessing import RLock, Manager

# Manager() class suppose to help manage inter-process data
# http://bit.ly/lPpO7

# man = Manager()

# define a global variable array
# globals = man.dict()
# globals['queue'] = []

# instruction set to be passed into runBlock()
# instr = """
# print(globals['queue'])
# """

# Lock() vs. RLock()
# http://bit.ly/w6ZnQu
# http://bit.ly/TQFzmd

# attempting to create a lock around the global dictionary

# l = RLock()
# def update(key, val):
#	l.acquire()
#	try:
#		d[key] = val
#	finally:
#		l.release()

# misc resources

# 'pickle' module apparently may also be useful
# http://bit.ly/VyrRBR

# Python decorators probabably will be needed
# http://bit.ly/1qoI77
# http://bit.ly/MNLS5Y
# http://bit.ly/qW0ak
# http://bit.ly/i5gM5
# http://ibm.co/VuocFc
