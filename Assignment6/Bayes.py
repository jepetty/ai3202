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
	
	cancerNode.conditionals["~PS"] = 0.05
	cancerNode.conditionals["~P~S"] = 0.02
	cancerNode.conditionals["PS"] = 0.03
	cancerNode.conditionals["P~S"] = 0.001
	xrayNode.conditionals["C"] = 0.9
	xrayNode.conditionals["~C"] = 0.2
	dyspnoeaNode.conditionals["C"] = 0.65
	dyspnoeaNode.conditionals["~C"] = 0.3
	
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
	length = len(arg)
	for i in range(0,length):
		if arg[i] == "P" or arg[i] == "p":
			node = network["pollution"]
			print("Pollution marginal probability: ", node.marginal)
			return node.marginal
		elif arg[i] == "S" or arg[i] == "s":
			node = network["smoker"]
			print ("Smoker marginal probability: ", node.marginal)
			return node.marginal
		elif arg[i] == "C" or arg[i] == "c":
			node = network["cancer"]
			conditionals = node.conditionals
			pollution = network["pollution"]
			smoker = network["smoker"]
			marginal = conditionals["~PS"]*(1-pollution.marginal)*(smoker.marginal) + conditionals["~P~S"]*(1-pollution.marginal)*(1-smoker.marginal) + conditionals["PS"]*pollution.marginal*smoker.marginal + conditionals["P~S"]*pollution.marginal*(1-smoker.marginal)
			print("Cancer marginal probability: ", marginal)
			return marginal
		elif arg[i] == "X" or arg[i] == "x":
			node = network["xray"]
			conditionals = node.conditionals
			cancerMarginal = calcMarginal(network, "C")
			marginal = conditionals["C"]*cancerMarginal + conditionals["~C"]*(1-cancerMarginal)
			print("Xray marginal probability: ", marginal)
			return marginal
		elif arg[i] == "D" or arg[i] == "d":
			node = network["dyspnoea"]
			conditionals = node.conditionals
			cancerMarginal = calcMarginal(network, "C")
			marginal = conditionals["C"]*cancerMarginal + conditionals["~C"]*(1-cancerMarginal)
			print("Dyspnoea marginal probability: ", marginal)
			return marginal
		else:
			print("Requesting marginal distribution for an invalid variable")
				
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
            calcMarginal(bayesNetwork, a)
        elif o in ("-g"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
            p = a.find("|")
            print(a[:p])
            print(a[p+1:])
			#calcConditional(a[:p], a[p+1:])
        elif o in ("-j"):
            print("flag: ", o)
            print("args: ", a)
            #calcJoint(o,a)
        else:
            assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()

