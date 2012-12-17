from multiprocessing import Process, Pipe, Manager, Queue
from classes.proc import Proc
from scripts.handler import handler
queue = Queue()
handler = Proc('handler', handler, {'queue' : queue, 'globals' : Manager().dict()})
handler.daemon = True
handler.start()
processes = Proc('processes', """procab = Proc('ab', \"\"\"
proc1 = Proc('ab_1', \\"\\"\\"SetReq('foo1', 'value1').send(self.var['queue'])

\\"\\"\\", {'queue' : self.var['queue']})
proc1.start()
proc1.join()
proc2 = Proc('ab_2', \\"\\"\\"SetReq('foo2', 'value2').send(self.var['queue'])
# note that foo1 is not initiated in this process
print(('value of foo1 is: %s') % (GetReq('foo1').recv(self.var['queue'])))
\\"\\"\\", {'queue' : self.var['queue']})
proc2.start()
proc2.join()
\"\"\", {'queue' : self.var['queue']})
procab.start()""", {'queue' : queue})
processes.start()
processes.join()
queue.put(None)
handler.join()
