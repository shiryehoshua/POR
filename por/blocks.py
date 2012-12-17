from classes.proc import Proc

# examples

# basic instruction set - triple quotes mark entire block as single string
sleep = """
import time, random
self.var['time'] = random.randint(0, 3)
time.sleep(self.var['time'])

# note that the instance variable is passed literally as if the instruction is sub'd into Proc.run()
#	i.e. the use of 'self' in this context refers to the process

print(('process %s slept for %s seconds') % (self.id, self.var['time']))
"""

# demonstrates the use of local variables in each process
rand = """
print(('process %s with var %s') % (self.id, self.var['rand']))
"""

def main():
	from lib.misc import runBlock, format
	import random, time

	# creates a block of 'sleep' Process() objects
	# the block of processes is also a Process() object
	sleepBlock = Proc('sleep', (('from lib.misc import runBlock\nrunBlock(%s, {})') % (format(sleep))))

	# note where the local variable dictionary goes in this invocation
	randBlock = Proc('random', (('from lib.misc import runBlock\nimport time, random\nrunBlock(%s, {\'rand\' : random.random()}), False') % (format(rand))))

	# the blocks here are run sequentially - though all processes within each block are concurrent
	print('running random sleep time block')
	sleepBlock.start()
	sleepBlock.join()

	print('running random init block')
	randBlock.start()
	randBlock.join()

main()
