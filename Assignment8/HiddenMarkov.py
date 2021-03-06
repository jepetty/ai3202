# Jessica Petty
# CSCI 3202
# November 13, 2015
# Assignment 8

import math

class State:
	def __init__(self, lett):
		self.letter = lett
		self.count = 0
		self.emissionCounts = {"a"+lett: 1, "b"+lett: 1, "c"+lett: 1, "d"+lett: 1, "e"+lett: 1, "f"+lett: 1, "g"+lett: 1, \
		"h"+lett: 1, "i"+lett: 1, "j"+lett: 1, "k"+lett: 1, "l"+lett: 1, "m"+lett: 1, "n"+lett: 1, "o"+lett: 1, \
		"p"+lett: 1, "q"+lett: 1, "r"+lett: 1, "s"+lett: 1, "t"+lett: 1, "u"+lett: 1, "v"+lett: 1, "w"+lett: 1, \
		"x"+lett: 1, "y"+lett: 1, "z"+lett: 1, "_"+lett: 1}
		self.emissions = {}
		self.transitionCounts = {lett+"a": 1, lett+"b": 1, lett+"c": 1, lett+"d": 1, lett+"e": 1, lett+"f": 1, lett+"g": 1, \
		lett+"h": 1, lett+"i": 1, lett+"j": 1, lett+"k": 1, lett+"l": 1, lett+"m": 1, lett+"n": 1, lett+"o": 1, \
		lett+"p": 1, lett+"q": 1, lett+"r": 1, lett+"s": 1, lett+"t": 1, lett+"u": 1, lett+"v": 1, lett+"w": 1, \
		lett+"x": 1, lett+"y": 1, lett+"z": 1, lett+"_": 1}
		self.transitions = {}
		self.dummy = 0

class Viterbi:
	def __init__(self):
		self.probStates = {}
		self.bpointers = {}

# Read in data from typos20.data
def parseData1():
	totalCount = 0.0
	f = open("typos20.data", "r")
	data = f.readlines()
	state = ""
	for line in data:
		# keep track of total count for dummy calculations
		totalCount = totalCount + 1.0
		# split into x actual value and e observed value
		(x, e) = line.split(" ")
		states[x].count = states[x].count + 1.0
		# Emission formated like e|x
		emission = e[0] + x
		states[x].emissionCounts[emission] = states[x].emissionCounts[emission] + 1.0
		if state != "":
			# Formatted like xt+1|x
			# Basically, for this x, what's the most likely next sequence of values
			transition = x + state
			states[x].transitionCounts[transition] = states[x].transitionCounts[transition] + 1.0
		state = x
	f.close()
	return totalCount

# Function to calculate the emission and transition probabilitites for each state
def calcProbabilities():
	for state in states:
		# calculate dummy probabilities
		states[state].dummy = (states[state].count + 1.0)/(totalCount + 27.0)
		for emission in states[state].emissionCounts:
			states[state].emissions[emission] = (states[state].emissionCounts[emission])/(states[state].count + 27)
		for transition in states[state].transitionCounts:
			states[state].transitions[transition] = (states[state].transitionCounts[transition])/(states[state].count + 27)

# Function to output the results of part 1 to a text file
def outputFunction1():
	f = open("outputFile.txt", "r+")
	f.write("Transition Probabilitites:\n")
	for state in states:
		for transition in states[state].transitions:
			newTrans = "P(" + transition[0] + "|" + transition[1] + ") = "
			f.write(newTrans + str(states[state].transitions[transition]) + "\n")
	f.write("Emission Probabilitites:\n")
	for state in states:
		for emission in states[state].emissions:
			newEmiss = "P(" + emission[0] + "|" + emission[1] + ") = "
			f.write(newEmiss + str(states[state].emissions[emission]) + "\n")
	f.write("Initial Probabilitites:\n")
	for state in states:
		f.write("P(" + state + ") = " + str(states[state].dummy) + "\n")
	f.close
	
# Function to parse the second data set we will be using for our Viterbi calculations	
def parseData2():
	f = open("typos20Test.data", "r")
	f.readline() # Need to ignore first line of text file -> Garbage!
	data = f.readlines()
	observed = []
	correct = []
	for line in data:
		(x,e) = line.split(" ")
		observed.append(e[0])
		correct.append(x)
	f.close
	return (observed, correct)

# Uses dummy probabilitites to calculate probabilitites for each state on first day, stores them in a new node
def calcFirstDay(observ):
	firstProbs = {}
	for state in states:
		emission = observ + states[state].letter
		# Using sum instead of product of probabilitites to keep numbers large		
		prob = math.log10(states[state].emissions[emission]) + math.log10(states[state].dummy)
		firstProbs[states[state].letter] = (prob, states[state].letter)
	vit = Viterbi()
	vit.probStates = firstProbs
	return vit

def calcDay(viterbis, observes):
	i = 0
	for observation in observes:
		vitNode = Viterbi()
		for x2State in states:
			maxProb = (-pow(10, 20), "")
			viterbiStates = viterbis[i].probStates
			for x1State in viterbiStates:
				(vProb, lett) = viterbiStates[x1State]
				prob = math.log10(states[x2State].emissions[observation+x2State]) + math.log10(states[x2State].transitions[x2State+x1State]) + vProb
				if (prob > maxProb[0]):
					maxProb = (prob, x1State)
			vitNode.probStates[x2State] = maxProb
		viterbis.append(vitNode)
		i = i + 1
	return viterbis

# Function to create the path from the calculated viterbis
def createPath(viterbis):
	totalNodes = len(viterbis)
	lastNode = viterbis[totalNodes-1]
	path = ""
	index = ""
	maxValue = (-pow(10, 20), "")
	for state in lastNode.probStates:
		if lastNode.probStates[state][0] > maxValue[0]:
			maxValue = lastNode.probStates[state]
			index = state
	path = index + path
	backpointer = maxValue[1]
	for i in range(0,totalNodes - 1):
		node = viterbis[totalNodes - 2 - i]
		(value, bp) = node.probStates[backpointer]
		path = backpointer + path
		backpointer = bp
	return path

# Create output function for the second part of the assignment
def outputFunction2(path, correctLett):
	pathLength = len(path)
	f = open("outputFile2.txt", "r+")
	wrongCount = 0.0
	for i in range(0, pathLength):
		f.write(path[i]+"\n")
		if path[i] != correctLett[i]:
			wrongCount = wrongCount + 1.0
	f.write("Error rate: " + str(wrongCount/pathLength))
	f.close

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
	outputFunction1()
	(obsStates, correct) = parseData2()
	viterbiNodes = []
	viterbiNodes.append(calcFirstDay(obsStates[0]))
	viterbiNodes = calcDay(viterbiNodes, obsStates[1:])
	viterbiPath = createPath(viterbiNodes)
	outputFunction2(viterbiPath, correct)







