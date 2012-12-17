# Parsing helpers
import random, time, re, sys

SEPARATOR = '|'

def parse(horizontalCode):
	lines = horizontalCode.split('\n')
	codeBlocks = {}
	i = 1
	while (len(lines[i]) > 0):
		partition = lines[i].partition(SEPARATOR)
		blockIndex = 0
		while (len(partition[1]) > 0):
			if (len(partition[0]) > 0):
				if (i == 1):
					codeBlocks[blockIndex] = partition[0]
					codeBlocks[blockIndex] += '\n' 
				else:
					codeBlocks[blockIndex] += partition[0]
					codeBlocks[blockIndex] += '\n'
				blockIndex += 1
			partition = partition[2].partition(SEPARATOR)
		if (i == 1):
			codeBlocks[blockIndex] = partition[0] + '\n'
		else:
			codeBlocks[blockIndex] += partition[0] + '\n'
		i+=1
	return codeBlocks.values()

class InterprettedCodeBlockInfo:
	def __init__(self, variables, codeBlock, changesData=False, accessesData=False):
		self.variables = variables
		self.codeBlock = codeBlock
		self.changesData = changesData
		self.accessesData = accessesData

	def getDependencies(self, otherInfo):
		dependencies = []
		for var in self.variables:
			if var in otherInfo.variables:
				dependencies.append(var)
		return dependencies

def interpret(codeBlock):
	# Variables will store all the global variables declared
	# in this codeBlock.
	variables = []
	lines = codeBlock.split('\n')
	changesData = False 
	accessesData = False

	# If there is nothing in this code block, just return
	if (not(lines)):
		return None 

	# Acquire all the global variables
	firstLine = lines[0].split()
	if (firstLine and firstLine[0] == 'global'):
		del firstLine[0]
		for var in firstLine:
			variables.append(var)

	# Replace instances of var with appropriate threaded things
	newCodeBlock = codeBlock
	for line in lines:
		for var in variables:
			# Replace all the instances of var = value with
			# SetReq('var', 'value').send(self.var['queue'])
			value = re.sub(r"^[\W]*" + var + "[\W]*=[\W]*", "", line)
			if value != line:
				newCodeBlock = re.sub(re.escape(line),
						"SetReq('" + var + "', " + 
						value + ").send(self.var['queue'])",
						newCodeBlock)
				changesData = True
			# Replace all the instances of var
			# GetReq('var').recv(self.var['queue']) 
			elif line != lines[0]:
				newLine = re.sub(var,
						"GetReq('" + var + "').recv(self.var['queue'])",
						line)
				if newLine != line:
					accessesData = True
				newCodeBlock = re.sub(re.escape(line), newLine, newCodeBlock)
	return InterprettedCodeBlockInfo(variables, newCodeBlock, changesData, accessesData) 

def createThreadFiles(horizontalCode):
	codeBlocks = parse(horizontalCode)
	interpretedCodeBlockInfos = []
	i = 0
	for codeBlock in codeBlocks:
		icbi = interpret(codeBlock)
		fp = open("./a_" + str(i) + ".thread", 'w+')
		fp.write(icbi.codeBlock)
		fp.close
		i += 1

# examples

horizontalCode = """
global x			|				|global x
import random			|import random			|import random
print "hey"			|print "whats up"		|i = x 
print "gorgeous"		|i = random.randint(1, 10)	|if (i < 5):
x = random.randint(1, 10)	|if (i > 5):			|	print "swolll"
print x				|	print "super swoll"	|
"""

def main():
	if len(sys.argv) == 2:
		fp = open(sys.argv[1], 'r')
		createThreadFiles(fp.read())
		fp.close()
	else:
		createThreadFiles(horizontalCode)
	print "done"

main()
