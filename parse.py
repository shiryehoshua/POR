# Parsing helpers
import random, time, re

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
		
def interpret(codeBlock):
	# Variables will store all the global variables declared
	# in this codeBlock.
	variables = []
	lines = codeBlock.split('\n')

	# If there is nothing in this code block, just return
	if (not(lines)):
		return

	# Acquire all the global variables
	firstLine = lines[0].split()
	if (firstLine and firstLine[0] == 'global'):
		del firstLine[0]
		for var in firstLine:
			variables.append(var)
		print variables

	# Replace instances of var with appropriate threaded things
	newCodeBlock = codeBlock
	for line in lines:
		for var in variables:
			# Replace all the instances of var = value with
			# SetReq('var', 'value').send(self.var['queue'])
			value = re.sub(r"^[\W]*" + var + "[\W]*=[\W]*", "", line)
			if value != line:
				newCodeBlock = re.sub(re.escape(line),
						"SetReq('" + var + "', '" + 
						value + "').send(self.var['queue'])",
						newCodeBlock)
			# Replace all the instances of var
			# GetReq('var').recv(self.var['queue']) 
			elif line != lines[0]:
				newLine = re.sub(var,
						"GetReq('" + var + "').recv(self.var['queue'])",
						line)
				newCodeBlock = re.sub(re.escape(line), newLine, newCodeBlock)
	return newCodeBlock		
		
		

# examples

horizontalCode = """
global x			|				|global x
print "hey"			|print "whats up"		|i = x 
print "gorgeous"		|i = random.randomint(1, 10)	|if (i < 5)
x = random.randomint(1, 10)	|if (i > 5):			|	print "swolll"
print x				|	print "super swoll"	|
"""

for codeBlock in parse(horizontalCode):
	print "---codeBlock---"
	print codeBlock
	print "---interpretation----"
	print interpret(codeBlock)
	
