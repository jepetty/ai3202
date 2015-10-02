# Jessica Petty
# CSCI 3202
# Assignment 5
# October 7, 2015

# Discount factor gamma = 0.9
# Reward of mountains = -1.0
# Reward of snakes = -2.0
# Reward of barn = 1.0
# Reward of apples = 50.0
# The value of epsilon in gamma < epsilon*(1-gamma)/gamma = 0.5

# Command-line arguments: Name of file and value for epsilon
# Output: Utility scores along optimal path, locations along optimal path


## Create a node class to create and store each location
class Node:
	def __init__(self):
		self.location = []
		self.distanceToStart = 0
		self.utility
		self.parent = None


## Read in command line arguments and assign to appropriate variables
filename = sys.argv[1]
fo = open(filename)
worldMatrix = []
lines = fo.readlines()
for line in lines:
	worldMatrix.append(line.split())
fo.close()
### TODO: Look up how to convert from arg string to double
epsilon = sys.argv[2]


