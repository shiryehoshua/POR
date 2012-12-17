from classes.req import GetReq, SetReq
from multiprocessing import Process

# each process is handled by a different CPU (ideally)
class Proc(Process):
	def __init__(self, id, instr = '', var = dict()):
		self.id = id

		# instructions to be run - note that instructions are all in 'one' line
		self.instr = str(instr)

		# list of local variables in a dictionary form
		self.var = var

		Process.__init__(self)

	def run(self):
		global queue

		# execute the instruction
		exec(self.instr)
