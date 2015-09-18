# Jessica Petty
# CSCI 3202
# Assignment 2
# September 18, 2015

import sys
import math

## Create nodes to add to a list
	# Location: (int, int)
	# distanceToStart: int
	# heuristic: int
	# f: int
	# parent: Node	
class Node:
	def __init__(self):
		self.location = []
		self.distanceToStart = 0
		self.heuristic = 0
		self.f = 0
		self.parent = None
	
	def adjacentNodes(self, world, heur):
		worldRowsCount = len(world)
		worldColumnsCount = len(world[0])
		adjacentList = []
		for i in range(-1, 2):
			if ((self.location[0] + i < worldRowsCount) and (self.location[0] + i >= 0)):
				for j in range (-1, 2):
					if ((self.location[1] + j < worldColumnsCount) and (self.location[1] + j >= 0)):
						node = Node()
						node.location = [self.location[0] + i, self.location[1] + j]
						node.parent = self
						node.distanceToStart = self.distanceToStart
						if (int(world[node.location[0]][node.location[1]]) == 2):
							continue
						elif (int(world[node.location[0]][node.location[1]]) == 1):
							if (i == -1 or i == 1) and (j == -1 or j == 1):
								node.distanceToStart = node.distanceToStart + 24
							elif (i == 0 and j == 0):
								continue
							else:
								node.distanceToStart = node.distanceToStart + 20
						if (int(world[node.location[0]][node.location[1]]) == 0):
							if (i == -1 or i == 1) and (j == -1 or j == 1):
								node.distanceToStart = node.distanceToStart + 14
							elif (i == 0 and j == 0):
								continue
							else:
								node.distanceToStart = node.distanceToStart + 10		
						if (heur == 1):
							node.heuristic = Manhattan(node.location, [0, worldColumnsCount -1])
						elif (heur == 2):
							node.heuristic = Euclidean(node.location, [0, worldColumnsCount - 1])
						else:	
							print("Not valid heuristic input")
							return -1
						node.f = node.distanceToStart + node.heuristic
						adjacentList.append(node)
		return adjacentList
				

## Helper functions
# Define heuristic using Manhattan distance
def Manhattan(location1, location2):
	value = abs(location2[0]-location1[0]) + abs(location2[1]-location1[1])
	return value * 10
def Euclidean(location1, location2):
	value = math.sqrt(pow(location2[0]-location1[0], 2) + pow(location2[1]-location1[1], 2))
	return value * 10

## Command line argument to read in files and then open and read data from world file
filename = sys.argv[1]
fo = open(filename)
worldMatrix = []
lines = fo.readlines()
for line in lines:
	worldMatrix.append(line.split())
fo.close()

heuristic = sys.argv[2]
heur = 0
if heuristic == "Manhattan":
	heur = 1
if heuristic == "Euclidean":
	heur = 2


## Calculate optimal path using AStar
# Creating start and end location for our nodes
def AStar(world, heur):
	worldRowsCount = len(world)
	worldColumnsCount = len(world[0])
	startNode = Node()
	startNode.location = [worldRowsCount - 1, 0]
	endNode = Node()
	endNode.location = [0, worldColumnsCount -1]
	startNode.heuristic = Manhattan(startNode.location, endNode.location)
	startNode.f = startNode.distanceToStart + startNode.heuristic
	openNodes = []
	openNodes.append(startNode)
	closedNodes = []
	while (len(openNodes) != 0):
		# finding minimum cost node in list of open nodes
		minimumCost = 10000
		nextNode = Node()
		for node in openNodes:
			if (node.f < minimumCost):
				nextNode = node
				minimumCost = nextNode.f
		openNodes.remove(nextNode)
		closedNodes.append(nextNode)
		if (nextNode.location != endNode.location):
			adjacent = nextNode.adjacentNodes(world, heur)
			if (adjacent == -1):
				print("No path found")
				return
			for node in adjacent:
				found = False
				if (node.location == nextNode.location):
					found = True
				for n in openNodes:
					if (n.location == node.location):
						if (n.f > node.f):
							n.f = node.f
							node.parent = nextNode
						found = True
				for n in closedNodes:
					if (n.location == node.location):
						found = True
				if (not found):
					openNodes.append(node)
					node.parent = nextNode
		else:
			print("Cost of the path: ", nextNode.distanceToStart)
			visitedNodes = [] 
			while (nextNode.parent is not None):
				visitedNodes.append(nextNode)
				nextNode = nextNode.parent
			visitedNodes.append(startNode)
			print("Location of visited nodes: ")
			length = len(visitedNodes) - 1
			while (length > -1):
				node = visitedNodes[length]
				print(node.location)
				length = length - 1
			print("Total visited nodes: ", len(visitedNodes))
			return

AStar(worldMatrix, heur)

	
	
	
	
	
	
	
	
	
