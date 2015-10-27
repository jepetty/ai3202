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
	
	pollutionNode.name = "pollution"
	smokerNode.name = "smoker"
	cancerNode.name = "cancer"
	xrayNode.name = "xray"
	dyspnoeaNode.name = "dyspnoea"
	
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
		marginal = conditionals["C"]*cancerMarginal[1] + conditionals["~c"]*(1-cancerMarginal[1])
		return ("Dyspnoea", marginal)
	else:
		print("Requesting marginal distribution for an invalid variable")

# Function to calculate the conditional probability
def calcConditional(network, arg, con):
	conLength = len(con)
	if arg == "p":
		node = network["pollution"]
	elif arg == "s":
		node = network["smoker"]
	elif arg == "c":
		node = network["cancer"]
		if con in node.conditionals:
			conditional = node.conditionals[con]
			return("Cancer", conditional)
	elif arg == "x":
		node = network["xray"]
		if con in node.conditionals:
			conditional = node.conditionals[con]
			return("Xray", conditional)
	elif arg == "d":
		node = network["dyspnoea"]
		if con in node.conditionals:
			conditional = node.conditionals[con]
			return("Dyspnoea", conditional)
	else:
		print("Requestion marginal distribution for an invalid variable")
			
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
            #calcJoint(o,a)
        else:
            assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()

