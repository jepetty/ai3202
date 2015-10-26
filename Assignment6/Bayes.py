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
		self.parents = None
		self.children = None

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
	
	cancerNode.conditionals["C|~PS"] = 0.05
	cancerNode.conditionals["C|~P~S"] = 0.02
	cancerNode.conditionals["C|PS"] = 0.03
	cancerNode.conditionals["C|P~S"] = 0.001
	xrayNode.conditionals["X|C"] = 0.9
	xrayNode.conditionals["X|~C"] = 0.2
	dyspnoeaNode.conditionals["D|C"] = 0.65
	dyspnoeaNode.conditionals["D|~C"] = 0.3
	
	nodeNetwork = [smokerNode, pollutionNode, cancerNode, xrayNode, dyspnoeaNode]
	return nodeNetwork
	
# Function to parse the argument from option list
def parseArgument(arg):
	# Parse the argument 
	print(arg)
	
# Main function to receive arguments, begin processing them
def main():
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
			#setting the prior here works if the Bayes net is already built
			#setPrior(a[0], float(a[1:])
        elif o in ("-m"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
			#calcMarginal(a)
        elif o in ("-g"):
            print("flag: ", o)
            print("args: ", a)
            print(type(a))
			# you may want to parse a here and pass the left of |
			# and right of | as arguments to calcConditional
            p = a.find("|")
            print(a[:p])
            print(a[p+1:])
			#calcConditional(a[:p], a[p+1:])
        elif o in ("-j"):
            print("flag: ", o)
            print("args: ", a)
        else:
            assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()

