# Parsing helpers
import random, time

SEPARATOR = '\t'

def parse(horizontalCode):
	lines = horizontalCode.split('\n')
	codeBlocks = {}
	i = 1
	while (len(lines[i]) > 0):
		partition = lines[i].partition(SEPARATOR)
		blockIndex = 0
		while (partition[1] == SEPARATOR):
			if (len(partition[0]) > 0):
				print "partition[0]: " + partition[0]
				print "blockIndex: " + str(blockIndex)
				if (i == 1):
					print "new string"
					codeBlocks[blockIndex] = partition[0]
					codeBlocks[blockIndex] += '\n' 
					print "codeBlocks[blockIndex]: " + codeBlocks[blockIndex]
				else:
					print "adding to string"
					codeBlocks[blockIndex] += partition[0]
					codeBlocks[blockIndex] += '\n'
				print "codeBlocks[blockIndex]: " + str(codeBlocks[blockIndex])
				blockIndex += 1
			partition = partition[2].partition(SEPARATOR)
		i+=1
	print codeBlocks
		

# examples
horizontalCode = """
print "hey"			print "whats up"		i = random.randint(1, 10)
print "gorgeous"		i = random.randomint(1, 10)	if (i < 5)
x = random.randomint(1, 10)	if (i > 5):				print "swolll":
print x					print "super swoll"
"""

parse (horizontalCode);
