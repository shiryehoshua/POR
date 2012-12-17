# daemon to handle shared variable requests
# all shared variables are physically located within this thread (self.var['globals'])
handler = """
while True:
	request = self.var['queue'].get()
	if(request == None):
		break
	else:
		# updates value
		if(request.method == 'set'):
			self.var['globals'][request.name] = request.value
		# returns value
		if(request.method == 'get'):
			pRes = request.decode(request.pRes)
			try:
				pRes.send(self.var['globals'][request.name])
			except KeyError:
				raise KeyError(\'key \\'%s\\' does not exist in the global variable scope\' % request.name)
			# closes input thread - no more information can be sent in this Pipe()
			# prevents requesting Req() from hanging while waiting for non-existent data
			pRes.close()
"""
