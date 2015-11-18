# Jessica Petty
# CSCI 3202
# November 13, 2015
# Assignment 8

class State:
	def __init__(self, lett):
		self.letter = lett
		self.count = 0
		self.trans = []
		self.evidence = []
		self.emissions = {}
		self.transitions = {}
		self.dummy = 0

class Viterbi:
	def __init__(self):
		self.letter = lett
		self.probStates = {}
		self.bpointer = ""
		self.max = 0

# Read in data from typos20.data
def parseData1():
	totalCount = 0.0
	f = open("typos20.data", "r")
	data = f.readlines()
	state = ""
	for line in data:
		# keep track of total count for dummy calculations
		totalCount = totalCount + 1.0
		(x, e) = line.split(" ")
		states[x].count = states[x].count + 1.0
		emission = x + e[0]
		if emission in states[x].emissions:
			states[x].emissions[emission] = states[x].emissions[emission] + 1.0
		else:
			states[x].evidence.append(emission)
			states[x].emissions[emission] = 1.0
		if state != "":
			transition = state + x
			if transition in states[x].transitions:
				states[x].transitions[transition] = states[x].transitions[transition] + 1.0
			else:
				states[x].trans.append(transition)
				states[x].transitions[transition] = 1.0
		state = x
	f.close()
	return totalCount

# Function to calculate the emission and transition probabilitites for each state
def calcProbabilities():
	for state in states:
		# calculate dummy probabilities
		states[state].dummy = (states[state].count + 1.0)/(totalCount + 27.0)
		for emission in states[state].evidence:
			states[state].emissions[emission] = (states[state].emissions[emission] + 1)/(states[state].count + len(states[state].evidence))
		for transition in states[state].trans:
			states[state].transitions[transition] = (states[state].transitions[transition] + 1)/(states[state].count + len(states[state].trans))

# Function to output the results of part 1 to a text file
def outputFunction1():
	f = open("outputFile.txt", "r+")
	f.write("P(Et | Xt)\n")
	for state in states:
		for emission in states[state].evidence:
			newEmiss = "P(" + emission[0] + " | " + emission[1] + ") = "
			f.write(newEmiss + str(states[state].emissions[emission]) + "\n")
	f.write("P(Xt+1 | Xt)\n")
	for state in states:
		for transition in states[state].trans:
			newTrans = "P(" + transition[0] + " | " + transition[1] + ") = "
			f.write(newTrans + str(states[state].transitions[transition]) + "\n")
	f.write("P(Xt)\n")
	for state in states:
		newState = "P(" + state + ") = "
		f.write(newState + str(states[state].dummy) + "\n")
	
# Function to parse the second data set we will be using for our Viterbi calculations	
def parseData2():
	f = open("typos20Test.data", "r")
	f.readline() # Need to ignore first line of text file -> Garbage!
	data = f.readlines()
	observed = []
	for line in data:
		(x,e) = line.split(" ")
		observed.append(e[0])
	f.close
	return observed


if __name__ == "__main__":
	# Create dictionaries to store number of states, probabilities, etc.
	states = { "_": State("_"), "a": State("a"), "b": State("b"),"c": State("c"), "d": State("d"), "e": State("e"), "f": State("f"),  \
		"g": State("g"), "h": State("h"), "i": State("i"), "j": State("j"), "k": State("k"), "l": State("l"), "m": State("m"), \
		"n": State("n"), "o": State("o"), "p": State("p"), "q": State("q"), "r": State("r"), "s": State("s"), "t": State("t"), \
		"u": State("u"), "v": State("v"), "w": State("w"), "x": State("x"), "y": State("y"), "z": State("z") }
	transitionCounts = {}
	emissionCounts = {}
	totalCount = parseData1()
	
	default = 1.0/(totalCount + 27.0)
	statesProbs = { "_": default, "a": default, "b": default,"c": default, "d": default, "e": default, "f": default,  \
		"g": default, "h": default, "i": default, "j": default, "k": default, "l": default, "m": default, "n": default, \
		"o": default, "p": default, "q": default, "r": default, "s": default, "t": default, "u": default, "v": default, \
		"w": default, "x": default, "y": default, "z": default }
	transitionProbs = {}
	emissionProbs = {}
	calcProbabilities()
	# outputFunction1()
	obsStates = parseData2()








