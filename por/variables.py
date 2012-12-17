from multiprocessing import Process, Pipe, Manager, Queue
from classes.proc import Proc

instr1 = """
SetReq('foo1', 'value1').send(self.var['queue'])
"""

instr2 = """
SetReq('foo2', 'value2').send(self.var['queue'])
# note that foo1 is not initiated in this process
print(('value of foo1 is: %s') % (GetReq('foo1').recv(self.var['queue'])))
"""

def main():
	from scripts.handler import handler

	# the queue is shared among all processes - Queue package handles synchronization
	queue = Queue()

	# handler logic to handle shared variables
	#	http://bit.ly/U1VNtT
	handler = Proc('reader', handler, {'queue' : queue, 'globals' : Manager().dict()})
	handler.daemon = True
	handler.start()

	proc1 = Proc('proc', instr1, {'queue' : queue})
	proc2 = Proc('proc', instr2, {'queue' : queue})

	proc1.start()
	proc1.join()
	proc2.start()
	proc2.join()

	# all processes have to finish before the final None queue input
	queue.put(None)
	handler.join()

main()
