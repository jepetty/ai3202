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

# Read in data from typos20.data
def parseData():
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

def calcProbabilities():
	for state in states:
		# calculate dummy probabilities
		states[state].dummy = (states[state].count + 1.0)/(totalCount + 27.0)
		for emission in states[state].evidence:
			states[state].emissions[emission] = (states[state].emissions[emission] + 1)/(states[state].count + len(states[state].evidence))
		for transition in states[state].trans:
			states[state].transitions[transition] = (states[state].transitions[transition] + 1)/(states[state].count + len(states[state].trans))


if __name__ == "__main__":
	# Create dictionaries to store number of states, probabilities, etc.
	states = { "_": State("_"), "a": State("a"), "b": State("b"),"c": State("c"), "d": State("d"), "e": State("e"), "f": State("f"),  \
		"g": State("g"), "h": State("h"), "i": State("i"), "j": State("j"), "k": State("k"), "l": State("l"), "m": State("m"), \
		"n": State("n"), "o": State("o"), "p": State("p"), "q": State("q"), "r": State("r"), "s": State("s"), "t": State("t"), \
		"u": State("u"), "v": State("v"), "w": State("w"), "x": State("x"), "y": State("y"), "z": State("z") }
	transitionCounts = {}
	emissionCounts = {}
	totalCount = parseData()
	
	default = 1.0/(totalCount + 27.0)
	statesProbs = { "_": default, "a": default, "b": default,"c": default, "d": default, "e": default, "f": default,  \
		"g": default, "h": default, "i": default, "j": default, "k": default, "l": default, "m": default, "n": default, \
		"o": default, "p": default, "q": default, "r": default, "s": default, "t": default, "u": default, "v": default, \
		"w": default, "x": default, "y": default, "z": default }
	transitionProbs = {}
	emissionProbs = {}
	calcProbabilities()








