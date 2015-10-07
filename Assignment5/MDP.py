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
		self.square = None


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
				node.utility = -1
				node.square = "Mountain"
			elif (int(world[i][j]) == 2):
				# Wall square
				node.reward = 0
				node.utility = 0
				node.action = None
				node.square = "Wall"
			elif (int(world[i][j]) == 3):
				# Snake square
				node.reward = -2
				node.utility = -2
				node.square = "Snake"
			elif (int(world[i][j]) == 4):
				# Barn square
				node.reward = 1
				node.utility = 1
				node.square = "Barn"
			elif (int(world[i][j]) == 50):
				# Goal square
				node.reward = 50
				node.utility = 50
				node.square = "Apple"
			else:
				node.square = "Normal"
			nodeMatrix[i][j] = node
	return nodeMatrix

def UpdateUtilityScores(nodes, e):
	delta = 100
	err = e/9
	nodesRowsCount = len(nodes)
	nodesColumnsCount = len(nodes[0])
	while (delta > err):
		delta = 0
		for i in range(0, nodesRowsCount):
			for j in range(0, nodesColumnsCount):
				node = nodes[i][j]
				# Calculate reward for each direction, taking into account if outside matrix bounds
				if node.square == "Wall":
					continue
				upReward = 0
				downReward = 0
				leftReward = 0
				rightReward = 0
				if ((i + 1) < nodesRowsCount):
					if (nodes[i+1][j]).square != "Wall":
						downNode = nodes[i+1][j]
						downReward = downNode.utility
				if ((i - 1) >= 0):
					if (nodes[i-1][j]).square != "Wall":
						upNode = nodes[i-1][j]
						upReward = upNode.utility
				if ((j + 1) < nodesColumnsCount):
					if (nodes[i][j+1]).square != "Wall":
						rightNode = nodes[i][j+1]
						rightReward = rightNode.utility
				if ((j - 1) >= 0):
					if (nodes[i][j-1]).square != "Wall":
						leftNode = nodes[i][j-1]
						leftReward = leftNode.utility
				# Calculate possible reward for moving in each direction
				moveUp = 0.8 * upReward + 0.1 * leftReward + 0.1 * rightReward
				moveDown = 0.8 * downReward + 0.1 * leftReward + 0.1 * rightReward
				moveLeft = 0.8 * leftReward + 0.1 * upReward + 0.1 * downReward
				moveRight = 0.8 * rightReward + 0.1 * upReward + 0.1 * downReward
				# Calculate which direction is the optimal direction to try and move
				if (moveUp >= moveDown) and (moveUp >= moveLeft) and (moveUp >= moveRight):
					oldUtility = node.utility
					node.action = "Up"
					node.utility = node.reward + 0.9 * moveUp
				elif (moveDown >= moveUp) and (moveDown >= moveLeft) and (moveDown >= moveRight):
					oldUtility = node.utility
					node.action = "Down"
					node.utility = node.reward + 0.9 * moveDown
				elif (moveLeft >= moveUp) and (moveLeft >= moveDown) and (moveLeft >= moveRight):
					oldUtility = node.utility
					node.action = "Left"
					node.utility = node.reward + 0.9 * moveLeft
				else:
					oldUtility = node.utility
					(nodes[i][j]).action = "Right"
					(nodes[i][j]).utility = node.reward + 0.9 * moveRight
				#nodes[i][j] = node
				# Update delta if a new smallest error is found
				if (delta < abs(node.utility - oldUtility)):
					delta = abs(node.utility - oldUtility)
	return nodes
	
def PrintPath(nodes):
	nodesRowsCount = len(nodes)
	nodesColumnsCount = len(nodes)
	node = nodes[nodesRowsCount - 1][0]
	while (node.reward != 50):
		print("Location: (", node.xlocation, ", ", node.ylocation, "), Utility: ", node.utility)
		if node.action == "Up":
			node = nodes[node.xlocation - 1][node.ylocation]
		elif node.action == "Down":
			node = nodes[node.xlocation + 1][node.ylocation]
		elif node.action == "Left":
			node = nodes[node.xlocation][node.ylocation - 1]
		else:
			node = nodes[node.xlocation][node.ylocation + 1]
	print("Location: (", node.xlocation, ", ", node.ylocation, "), Utility: ", node.utility)
			
	
nodeMatrix = CreateNodeMatrix(worldMatrix)
updatedMatrix = UpdateUtilityScores(nodeMatrix, epsilon)
PrintPath(updatedMatrix)


