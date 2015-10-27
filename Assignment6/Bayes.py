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
		self.children = []

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
	
	pollutionNode.children.append(cancerNode)
	smokerNode.children.append(cancerNode)
	cancerNode.children.append(xrayNode)
	cancerNode.children.append(dyspnoeaNode)
	
	cancerNode.parents.append(smokerNode)
	cancerNode.parents.append(pollutionNode)
	xrayNode.parents.append(cancerNode)
	dyspnoeaNode.parents.append(cancerNode)
	
	pollutionNode.marginal = 0.9
	smokerNode.marginal = 0.3
	
	cancerNode.conditionals["~ps"] = 0.05
	cancerNode.conditionals["~p~s"] = 0.02
	cancerNode.conditionals["ps"] = 0.03
	cancerNode.conditionals["p~s"] = 0.001
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
	if arg[0] == '~':
		marginal = calcMarginal(network, arg[1])
		return ("Not " + marginal[0], 1 - marginal[1])
	if arg == "P" or arg == "p":
		node = network["pollution"]
		return ("Pollution", node.marginal)
	elif arg == "S" or arg == "s":
		node = network["smoker"]
		return ("Smoker", node.marginal)
	elif arg == "C" or arg == "c":
		node = network["cancer"]
		conditionals = node.conditionals
		pollution = network["pollution"]
		smoker = network["smoker"]
		marginal = conditionals["~ps"]*(1-pollution.marginal)*(smoker.marginal) + conditionals["~p~s"]*(1-pollution.marginal)*(1-smoker.marginal) + conditionals["ps"]*pollution.marginal*smoker.marginal + conditionals["p~s"]*pollution.marginal*(1-smoker.marginal)
		return ("Cancer", marginal)
	elif arg == "X" or arg == "x":
		node = network["xray"]
		conditionals = node.conditionals
		cancerMarginal = calcMarginal(network, "C")
		marginal = conditionals["c"]*cancerMarginal[1] + conditionals["~c"]*(1-cancerMarginal[1])
		return ("Xray", marginal)
	elif arg == "D" or arg == "d":
		node = network["dyspnoea"]
		conditionals = node.conditionals
		cancerMarginal = calcMarginal(network, "c")
		marginal = conditionals["c"]*cancerMarginal[1] + conditionals["~c"]*(1-cancerMarginal[1])
		return ("Dyspnoea", marginal)
	else:
		print("Requesting marginal distribution for an invalid variable")

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
		arg = arg[1]
	conList = parseVariables(con)
	if arg == "p":
		node = network["pollution"]
	elif arg == "s":
		node = network["smoker"]
	elif arg == "c":
		node = network["cancer"]
	elif arg == "x":
		node = network["xray"]
	elif arg == "d":
		node = network["dyspnoea"]
	else:
		print("Requesting conditional distribution for an invalid variable: ", arg)
	# Remove once you have this implemented ***********
	conditional = 1
	if (len(con) == 0):
		conditional = calcMarginal(network, arg)[1]
	elif con in node.conditionals:
		conditional = node.conditionals[con]
	if notBool:
		return 1 - conditional
	else:
		return conditional
	return 1
			
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
            print(marginal[0], " marginal probability: ", marginal[1])
        elif o in ("-g"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
            p = a.find("|")
            print(a[:p])
            print(a[p+1:])
            conditional = calcConditional(bayesNetwork, a[:p], a[p+1:])
            print(conditional[0], " conditional probability: ", conditional[1])
        elif o in ("-j"):
            print("flag: ", o)
            print("args: ", a)
            print(calcJointDistribution(bayesNetwork, a))
        else:
            assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()

