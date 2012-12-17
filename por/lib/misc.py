# run a block of identical processes
def runBlock(instr, var, concurrent = True):
	from classes.proc import Proc
	for id in xrange(10):
		# init 10 processes
		proc = Proc(id, instr, var)
		proc.start()
		# .join() enforces current process to finish before iterating
		if(not(concurrent)):
			proc.join()

# wraps the instructions in a deeper level of quotes
def format(instr):
	return(('"""%s"""') % (instr.replace('"""', '\"\"\"')))
