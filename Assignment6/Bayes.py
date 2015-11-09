# Jessica Petty
# CSCI 3202
# Assignment 6
# October 23, 2015

import getopt
import sys

# Define node class to represent each node in the Bayes Net
class Node:
	def __init__(self):
		self.marginal = 0
		self.conditionals = {}
		self.name = ""
		self.parents = []
		self.grandparents = []
		self.children = []
		self.grandchildren = []

# Function to create the Bayes network with appropriate nodes
def createNetwork():
	pollutionNode = Node()
	smokerNode = Node()
	cancerNode = Node()
	xrayNode = Node()
	dyspnoeaNode = Node()
	
	pollutionNode.name = "p"
	smokerNode.name = "s"
	cancerNode.name = "c"
	xrayNode.name = "x"
	dyspnoeaNode.name = "d"
	
	pollutionNode.children.append("c")
	smokerNode.children.append("c")
	cancerNode.children.append("x")
	cancerNode.children.append("d")
	
	pollutionNode.grandchildren.append("x")
	pollutionNode.grandchildren.append("d")
	smokerNode.grandchildren.append("x")
	smokerNode.grandchildren.append("d")
	
	cancerNode.parents.append("s")
	cancerNode.parents.append("p")
	xrayNode.parents.append("c")
	dyspnoeaNode.parents.append("c")
	
	xrayNode.grandparents.append("p")
	xrayNode.grandparents.append("s")
	dyspnoeaNode.grandparents.append("p")
	dyspnoeaNode.grandparents.append("s")
	
	pollutionNode.marginal = 0.9
	smokerNode.marginal = 0.3
	
	cancerNode.conditionals["~ps"] = 0.05
	cancerNode.conditionals["s~p"] = 0.05
	cancerNode.conditionals["~p~s"] = 0.02
	cancerNode.conditionals["~s~p"] = 0.02
	cancerNode.conditionals["ps"] = 0.03
	cancerNode.conditionals["sp"] = 0.03
	cancerNode.conditionals["p~s"] = 0.001
	cancerNode.conditionals["~sp"] = 0.001
	xrayNode.conditionals["c"] = 0.9
	xrayNode.conditionals["~c"] = 0.2
	dyspnoeaNode.conditionals["c"] = 0.65
	dyspnoeaNode.conditionals["~c"] = 0.3
	
	nodeNetwork = {"smoker": smokerNode, "pollution": pollutionNode, "cancer": cancerNode, "xray": xrayNode, "dyspnoea": dyspnoeaNode}
	return nodeNetwork
	
def setPrior(network, arg, value):
	if arg == "p" or arg == "P":
		node = network["pollution"]
		node.marginal = value
	elif arg == "s" or arg == "S":
		node = network["smoker"]
		node.marginal = value
	else:
		print("Cannot set the prior for this variable")
	
def calcMarginal(network, arg):
	notBool = False
	if arg[0] == "~":
		notBool = True
		arg = arg[1]
	if arg == "P" or arg == "p":
		node = network["pollution"]
		marginal = node.marginal
	elif arg == "S" or arg == "s":
		node = network["smoker"]
		marginal = node.marginal
	elif arg == "C" or arg == "c":
		node = network["cancer"]
		conditionals = node.conditionals
		pollution = network["pollution"]
		smoker = network["smoker"]
		marginal = conditionals["~ps"]*(1-pollution.marginal)*(smoker.marginal) + conditionals["~p~s"]*(1-pollution.marginal)*(1-smoker.marginal) + conditionals["ps"]*pollution.marginal*smoker.marginal + conditionals["p~s"]*pollution.marginal*(1-smoker.marginal)
	elif arg == "X" or arg == "x":
		node = network["xray"]
		conditionals = node.conditionals
		cancerMarginal = calcMarginal(network, "C")
		marginal = conditionals["c"]*cancerMarginal + conditionals["~c"]*(1-cancerMarginal)
	elif arg == "D" or arg == "d":
		node = network["dyspnoea"]
		conditionals = node.conditionals
		cancerMarginal = calcMarginal(network, "c")
		marginal = conditionals["c"]*cancerMarginal + conditionals["~c"]*(1-cancerMarginal)
	else:
		print("Requesting marginal distribution for an invalid variable")
		return 0
	if notBool == True:
		return 1-marginal
	else:
		return marginal

# Helper function to parse the variables included in the joint probability
def parseJoint(arg):
	jointVarList = []
	newArg = ""
	argLength = len(arg)
	i = 0
	while (i < argLength):
		if arg[i] == "~":
			i = i + 1
		newArg = newArg + arg[i].lower()
		i = i + 1
	length = len(newArg)
	for i in range(0, length):
		newVar = []
		if len(jointVarList) == 0:
			newVar.append(newArg[i])
			newVar.append("~" + newArg[i])
		else: 
		    for var in jointVarList:
			    newVar.append(var + newArg[i])
			    newVar.append(var + "~" + newArg[i])
		jointVarList = newVar
	return jointVarList

# Function to calculate and return the joint probability
def calcJointDistribution(network, arg):
	variableList = parseJoint(arg)
	probabilities = {}
	if arg in variableList:
		return calcJointProbability(network, arg)
	else:
	    for var in variableList: 
		    probabilities[var] = calcJointProbability(network, var)
	    return probabilities

# Function to calculate the probability for individual, specific joint cases
def calcJointProbability(network, arg):
	probability = 1
	length = len(arg)
	i = 0
	while (i < length):
		if arg[i] == "~":
			i = i + 1
			newArg = "~" + arg[i]
			probability = probability * calcConditional(network, newArg, arg[i+1:])
		else:
			probability = probability * calcConditional(network, arg[i], arg[i+1:])
		i = i + 1
	return probability	

# Function to parse variables for conditional probability function
def parseVariables(variables):
	varList = []
	length = len(variables)
	i = 0
	while (i < length):
		if variables[i] == '~':
			i = i + 1
			var = variables[i-1] + variables[i]
			varList.append(var)
		else:
			varList.append(variables[i])
		i = i + 1
	return varList

# Function to calculate the conditional probability
def calcConditional(network, arg, con):
	notBool = False
	if arg[0] == '~':
		notBool = True
		newArg = arg[1]
	else:
		newArg = arg
	conList = parseVariables(con)
	if newArg == "p":
		node = network["pollution"]
	elif newArg == "s":
		node = network["smoker"]
	elif newArg == "c":
		node = network["cancer"]
	elif newArg == "x":
		node = network["xray"]
	elif newArg == "d":
		node = network["dyspnoea"]
	else:
		print("Requesting conditional distribution for an invalid variable: ", arg)
	if (len(conList) == 0):
		return calcMarginal(network, arg)
	elif con in node.conditionals:
		conditional = node.conditionals[con]
	elif (len(conList) == 1):
		conditional = calcCondOne(node, network, conList[0])
	elif (len(conList) == 2):
		return calcCondTwo(arg, network, conList)
	elif (len(conList) == 3):
		conditional = calcCondThree(arg, network, conList)
	if notBool:
		return 1 - conditional
	else:
		return conditional
	return conditional

# Helper function when conditional calculation is needed with one conditional
def calcCondOne(node, network, con):
	notBool = False
	if con[0] == "~":
		notBool = True
		newCon = con[1]
	else:
		newCon = con
	arg = node.name
	if arg == newCon:
		if notBool:
			return 0
		else:
			return 1
	if arg == "p" or arg == "s":
		if newCon == "p" or newCon == "s":
			return calcMarginal(network, arg)
		elif newCon == "c":
			return (calcConditional(network, con, arg)*calcMarginal(network, arg))/calcMarginal(network, con)
		elif newCon == "d" or newCon == "x":
			cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", con)
			cond2 = calcConditional(network, arg, "~c")*calcConditional(network, "~c", con)
			return cond1 + cond2
	elif arg == "c":
		if newCon == "p":
			return calcConditional(network, arg, con+"s")*calcMarginal(network, "s") + calcConditional(network, arg, con + "~s")*calcMarginal(network, "~s")
		elif newCon == "s":
			return calcConditional(network, arg, con+"p")*calcMarginal(network, "p") + calcConditional(network, arg, con + "~p")*calcMarginal(network, "~p")
		elif newCon == "d" or newCon == "x":
			return (calcConditional(network, con, arg)*calcMarginal(network, arg))/calcMarginal(network, con)
	elif arg == "d" or arg == "x":
		if newCon == "d" or newCon == "x":
			cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", con)
			cond2 = calcConditional(network, arg, "~c") * calcConditional(network, "~c", con)
			return cond1 + cond2
		elif newCon == "s" or newCon == "p":
			cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", con)
			cond2 = calcConditional(network, arg, "~c") * calcConditional(network, "~c", con)
			return cond1 + cond2
	
def calcCondTwo(arg, network, conditionals):
	conditional1 = conditionals[0]
	conditional2 = conditionals[1]
	if conditional1[0] == "~":
		newCon1 = conditional1[1]
	else:
		newCon1 = conditional1
	if conditional2[0] == "~":
		newCon2 = conditional2[1]
	else:
		newCon2 = conditional2
	if arg[0] == "~":
		newArg = arg[1]
	else:
		newArg = arg
	if newArg == "p" or newArg == "s":
		if newCon1 == "x" or newCon2 == "d":
			if newCon2 == "x" or newCon2 == "d":
				# Case 2
				cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", conditionals[0]+conditionals[1])
				cond2 = calcConditional(network, arg, "~c")*calcConditional(network, "~c", conditionals[0]+conditionals[1])
				return cond1 + cond2
			elif newCon2 == "s" or newCon2 == "p":
				# Case 3
				cond1 = calcConditional(network, arg, conditionals[1] + "c")*calcConditional(network, "c", conditionals[1]+conditionals[0])
				cond2 = calcConditional(network, arg, conditionals[1] + "~c")*calcConditional(network, "~c", conditionals[1]+conditionals[0])
				return cond1 + cond2
			elif newCon2 == "c":
				# Case 4
				return calcConditional(network, arg, conditionals[1])
		elif newCon1 == "p" or newCon1 == "s":
			if newCon2 == "c":
				# Case 1
				condNum = calcConditional(network, conditionals[1], arg + conditionals[0])*calcJointProbability(network, arg + conditionals[0])
				condDen = calcConditional(network, conditionals[0], conditionals[1])*calcMarginal(network, conditionals[1])
				return condNum/condDen
			elif newCon2 == "x" or newCon2 == "d":
				# Case 3
				cond1 = calcConditional(network, arg, conditionals[0] + "c")*calcConditional(network, "c", conditionals[1]+conditionals[0])
				cond2 = calcConditional(network, arg, conditionals[0] + "~c")*calcConditional(network, "~c", conditionals[1]+conditionals[0])
				return cond1 + cond2
		elif newCon1 == "c":
			if newCon2 == "x" or newCon2 == "d":
				return calcConditional(network, arg, conditionals[0])
			elif newCon2 == "s" or newCon2 == "p":
				# Case 1
				condNum = calcConditional(network, conditionals[0], arg + conditionals[1])*calcJointProbability(network, arg + conditionals[1])
				condDen = calcConditional(network, conditionals[1], conditionals[0])*calcMarginal(network, conditionals[0])
				return condNum/condDen
	elif newArg == "c":
		if newCon1 == "x" or newCon1 == "d":
			return calcConditional(network, arg, conditionals[1])
		elif newCon2 == "x" or newCon2 == "d":
			return calcConditional(network, arg, conditionals[0])
		else:
			condNum = calcConditional(network, conditionals[0], conditionals[1]) * calcJointProbability(network, arg + conditionals[0])
			condDen = calcMarginal(network, conditionals[0]) * calcMarginal(network, conditionals[1])
			return condNum/condDen
	elif newArg == "d" or newArg == "x":
		if newCon1 == "x" or newCon1 == "d":
			if newCon2 == "c":
				return calcConditional(network, arg, conditionals[1])
			else:
				cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", conditionals[1])
				cond2 = calcConditional(network, arg, "~c")*calcConditional(network, "~c", conditionals[1])
				return cond1 + cond2
		elif newCon1 == "c":
			if newCon2 == "x" or newCon2 == "d":
				return calcConditional(network, arg, conditionals[0])
			elif newCon2 == "s" or newCon2 == "p":
				return calcConditional(network, arg, conditionals[0])
		elif newCon1 == "p" or newCon2 == "s":
			if newCon2 == "s" or newCon2 == "p":
				cond1 = calcConditional(network, arg, "c") * calcConditional(network, "c", conditionals[0]+conditionals[1])
				cond2 = calcConditional(network, arg, "~c") * calcConditional(network, "~c", conditionals[0]+conditionals[1])
				return cond1 + cond2
			elif newCon2 == "d" or newCon2 == "x":
				cond1 = calcConditional(network, arg, "c")*calcConditional(network, "c", conditionals[0])
				cond2 = calcConditional(network, arg, "~c")*calcConditional(network, "~c", conditionals[0])
				return cond1 + cond2
			elif newCon2 == "c": 
				return calcConditional(network, arg, conditionals[1])

def calcCondThree(arg, network, conditionals):
	conditional1 = conditionals[0]
	conditional2 = conditionals[1]
	conditional3 = conditionals[2]
	if conditional1[0] == "~":
		newCon1 = conditional1[1]
	else:
		newCon1 = conditional1
	if conditional2[0] == "~":
		newCon2 = conditional[1]
	else:
		newCon2 = conditional2
	if conditional3[0] == "~":
		newCon3 = conditional3[1]
	else:
		newCon3 = conditional3
	if arg[0] == "~":
		newArg = arg[1]
	else:
		newArg = arg	
	if newArg == "s" or newArg == "p":
		if newCon1 == "p" or newCon1 == "s":
			if newCon2 == "x" or newCon2 == "d":
				if newCon3 == "x" or newCon3 == "d":
					# Case T2
					cond1 = calcConditional(network, arg, conditional1 + "c")*calcConditional(network, "c", conditional2 + conditional3)
					cond2 = calcConditional(network, arg, conditional1 + "~c")*calcConditional(network, "~c", conditional2 + conditional3)
					return cond1 + cond2
				elif newCon3 == "c":
					# Case T1
					return calcConditional(network, arg, conditional3+conditional1)
			elif newCon2 == "c":
				# Case T1
				return calcConditional(network, arg, conditional2 + conditional1)
		elif newCon1 == "d" or newCon1 == "x":
			if newCon2 == "d" or newCon2 == "s":
				if newCon3 == "p" or newCon3 == "s":
					# Case T2
					cond1 = calcConditional(network, arg, conditional3 + "c")*calcConditional(network, "c", conditional1+conditional2)
					cond2 = calcConditional(network, arg, conditional3 + "~c")*calcConditional(network, "~c", conditional1+conditional2)
					return cond1 + cond2
				elif newCon3 == "c":
					# Case T3
					return calcConditional(network, arg, conditional3)
			elif newCon2 == "c":
				if newCon3 == "p" or newCon3 == "s":
					# Case T1
					return calcConditional(network, arg, conditional3 + conditional2)
				elif newCon3 == "d" or newCon3 == "x":
					# Case T3
					return calcConditional(network, arg, conditional3)
		elif newCon1 == "c":
			if newCon2 == "d" or newCon2 == "x":
				if newCon3 == "d" or newCon3 == "x":
					# Case T3
					return calcConditional(network, arg, conditional1)
				elif newCon3 == "p" or newCon3 == "s":
					# Case T1
					return calcConditional(network, arg, conditional1 + conditional3)
			elif newCon2 == "s" or newCon2 == "p":
				# Case T1
				return calcConditional(network, arg, conditional1 + conditional2)
				
	elif newArg == "c":
		if newCon1 == "p" or newCon1 == "s":
			if newCon2 == "p" or newCon2 == "s" or newCon3 == "p" or newCon3 == "s":
				# Case M1
				return calcConditional(network, arg, conditional1+conditional2)
			else:
				# Case M2
				return calcConditional(network, arg, conditional1 + conditional2)
		elif newCon1 == "d" or newCon1 == "x":
			if newCon2 == "d" or newCon2 == "x" or newCon3 == "d" or newCon3 == "x":
				# Case M2
				return calcConditional(network, arg, conditional2 + conditional3)
			else:
				# Case M1
				return calcConditional(network, arg, conditional2 + conditional3)
	elif newArg == "d" or newArg == "x":
		if newCon1 == "p" or newCon1 == "s":
			if newCon2 == "p" or newCon2 == "s":
				if newCon3 == "c":
					# Case B1
					return calcConditional(network, arg, conditional3)
				elif newCon3 == "d" or newCon3 == "x":
					# Case B3
					cond1 = calcConditional(network, arg, "c" + conditional3)*calcConditional(network, "c", conditional2 + conditional1)
					cond2 = calcConditional(network, arg, "~c" + conditional3)*calcConditional(network, "~c", conditional2 + conditional1)
					return cond1 + cond2
			elif newCon2 == "d" or newCon2 == "x":
				if newCon3 == "c":
					# Case B2
					calcConditional(network, arg, conditional3)
				elif newCon3 == "s" or newCon3 == "p":
					# Case B3
					cond1 = calcConditional(network, arg, condition2 + "c") * calcConditional(network, "c", condition1 + condition3)
					cond2 = calcConditional(network, arg, condition2 + "~c") * calcConditional(network, "~c", condition1 + condition3)
			elif newCon2 == "c":
				if newCon3 == "x" or newCon3 == "d":
					# Case B2
					return calcConditional(network, arg, conditional2)
				elif newCon3 == "s" or newCon3 == "p":
					# Case B1
					return calcConditonal(network, arg, conditional2)
		elif newCon1 == "d" or newCon1 == "x":
			if newCon2 == "c" or newCon3 == "c":
				# Case B2
				return calcConditional(network, arg, conditional2)
			else:
				# Case B3
				cond1 = calcConditional(network, arg, condition1 + "c") * calcConditional(network, "c", condition2 + condition3)
				cond2 = calcConditional(network, arg, condition1 + "~c") * calcConditional(network, "~c", condition2 + condition3)
		elif newCon1 == "c":
			if newCon2 == "d" or newCon2 == "x" or newCon3 == "d" or newCon3 == "x":
				# Case B2
				return calcConditional(network, arg, conditional1)
			else:
				# Case B1
				return calcConditional(network, arg, conditional1)
	
# Main function to receive arguments, begin processing them
def main():
    bayesNetwork = createNetwork()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o in ("-p"):
            print("flag: ", o)
            print("args: ", a)
            print(a[0])
            print(float(a[1:]))
            setPrior(bayesNetwork, a[0], float(a[1:]))
        elif o in ("-m"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
            marginal = calcMarginal(bayesNetwork, a)
            print("marginal", a, marginal)
        elif o in ("-g"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
            p = a.find("|")
            print(a[:p])
            print(a[p+1:])
            conditional = calcConditional(bayesNetwork, a[:p], a[p+1:])
            print("conditional", a, conditional)
        elif o in ("-j"):
            print("flag: ", o)
            print("args: ", a)
            print(calcJointDistribution(bayesNetwork, a))
        else:
            assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()

