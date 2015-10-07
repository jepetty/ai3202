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

import sys
import math

## Create a node class to create and store each location
class Node:
	def __init__(self):
		self.xlocation = -1
		self.ylocation = -1
		self.reward = 0
		self.utility = 0
		self.action = None


## Read in command line arguments and assign to appropriate variables
filename = sys.argv[1]
fo = open(filename)
worldMatrix = []
lines = fo.readlines()
for line in lines:
	worldMatrix.append(line.split())
fo.close()
epsilon = float(sys.argv[2])

# Function to create a matrix with nodes corresponding to world
def CreateNodeMatrix(world):
	worldRowsCount = len(world)
	worldColumnsCount = len(world[0])
	nodeMatrix = world
	for i in range(0, worldRowsCount):
		for j in range(0, worldColumnsCount):
			node = Node()
			node.utility = 0
			node.xlocation = i
			node.ylocation = j
			if (int(world[i][j]) == 1):
				# Mountain square
				node.reward = -1
			elif (int(world[i][j]) == 2):
				# Wall square
				node.reward = -100000
				node.utility = -100000
				node.action = None
			elif (int(world[i][j]) == 3):
				# Snake square
				node.reward = -2
			elif (int(world[i][j]) == 4):
				# Barn square
				node.reward = 1
			elif (int(world[i][j]) == 50):
				# Goal square
				node.reward = 50
				node.utility = 50
			nodeMatrix[i][j] = node
	return nodeMatrix

def UpdateUtilityScores(nodes, e):
	delta = 1000000
	err = e/9
	nodesRowsCount = len(nodes)
	nodesColumnsCount = len(nodes[0])
	while (delta > err):
		for i in range(0, nodesRowsCount):
			for j in range(0, nodesColumnsCount):
				if ((i + 1) <= nodesRowsCount):
					# go up
					upNode = nodes[i+1][j]
					upReward = upNode.reward
				else:
					upReward = 0
				if ((i - 1) >= 0):
					downNode = nodes[i-1][j]
					downReward = downNode.reward
				else:
					downReward = 0
				if ((j + 1) <= nodesColumnsCount):
					rightNode = nodes[i][j+1]
					rightReward = rightNode.reward
				else:
					rightReward = 0
				if ((j - 1) >= 0):
					leftNode = nodes[i][j-1]
					leftReward = leftNode.reward
				else:
					leftReward = 0
	
nodeMatrix = createPathMatrix(worldMatrix)
updateUtilityScores(nodeMatrix, epsilon)


