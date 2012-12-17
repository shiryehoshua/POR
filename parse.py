# Parsing helpers
import random, time

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
		

# examples
horizontalCode = """
print "hey"			|print "whats up"		|i = random.randint(1, 10)
print "gorgeous"		|i = random.randomint(1, 10)	|if (i < 5)
x = random.randomint(1, 10)	|if (i > 5):			|	print "swolll"
print x				|	print "super swoll"	|
"""

for codeBlock in parse(horizontalCode):
	print codeBlock
	
