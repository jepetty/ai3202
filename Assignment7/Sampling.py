# Jessica Petty
# CSCI 3202
# Assignment 7
# November 4, 2015

import sys

# Create the Bayes network for this problem
# Define node class to represent each node in the Bayes Net
class Node:
	def __init__(self):
		self.marginal = 0
		self.conditionals = {}
		self.name = ""

# Function to create the Bayes net with the proper nodes
def createNetwork():
	cloudNode = Node()
	sprinklerNode = Node()
	rainNode = Node()
	grassNode = Node()
	
	cloudNode.name = "c"
	sprinklerNode.name = "s"
	rainNode.name = "r"
	grassNode.name = "w"
	
	cloudNode.marginal = 0.5
	
	sprinklerNode.conditionals = {"c": 0.1, "~c": 0.5}
	rainNode.conditionals = {"c": 0.8, "~c": 0.2}
	grassNode.conditionals = {"sr": 0.99, "s~r": 0.9, "~sr": 0.9, "~s~r": 0} 
	
	return {"c": cloudNode, "s": sprinklerNode, "r": rainNode, "w": grassNode}
	

# Create main function to run program
def main():
	network = createNetwork()

if __name__ == "__main__":
    main()


	
	
	
	
	
	
	
	
	
	
