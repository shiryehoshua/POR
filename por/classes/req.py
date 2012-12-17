from multiprocessing import Pipe, Queue
from multiprocessing.reduction import reduce_connection
from pickle import loads, dumps

# request classes

# the base request class
class Req():
	def __init__(self, method, name):
		self.method = method
		self.name = name

		# Queue() objects can't handle embedded Pipe() objects
		# must 'pickle' each connection into a string
		#	http://bit.ly/Y9E0nj
		if(self.method == 'get'):
			(pReq, pRes) = Pipe(False)
			self.pReq = self.encode(pReq)
			self.pRes = self.encode(pRes)

	# decode: String -> Connection
	def decode(self, pickle):
		# converts string into pickled Connection()
		unpickle = loads(pickle)
		# inflates into Connection()
		return(unpickle[0](*unpickle[1]))

	# encode: Connection -> String
	def encode(self, connection):
		# reduces Connection() objects to pickleable objects
		reduced = reduce_connection(connection)
		# pickles the Connection() into a string
		return(dumps(reduced))

# establishes a set request - updates a global variable
class SetReq(Req):
	def __init__(self, name, value):
		self.value = value
		Req.__init__(self, 'set', name)

	def send(self, queue):
		# request is handled by stuff
		queue.put(self)

# establishes a get request - returns a global variable
class GetReq(Req):
	def __init__(self, name):
		Req.__init__(self, 'get', name)

	# gets value of self.name from global dict
	def recv(self, queue):
		queue.put(self)
		pReq = self.decode(self.pReq)
		value = pReq.recv()
		pReq.close()
		return(value)
