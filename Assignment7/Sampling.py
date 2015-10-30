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

# 0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]
# Hard code sample data into program
samples = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28, 1, 0.95, 0.71, 0.14, 0.1, 1.0, \
	0.71, 0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97, 0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, \
	0.14, 0.13, 0.4, 0.94, 0.19, 0.6, 0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, \
	0.11, 0.83, 0.96, 0.41, 0.65, 0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97, 0.95, 0.01, 0.62, 0.32, \
	0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

def Problem1():
	sampleSize = len(samples)
	sample1 = []
	cloudy = False
	sprinkling = False
	raining = False
	wetGrass = False
	i = 0
	while i < sampleSize:
		if samples[i] < 0.5:
			cloudy = True
		i = i + 1
		if cloudy == True:
			if samples[i] < 0.1:
				sprinkling = True
			if samples[i+1] < 0.8:
				raining = True
		else:
			if samples[i] < 0.5:
				sprinkling = True
			if samples[i+1] < 0.2:
				raining = True
		i = i + 2
		if sprinkling == True and raining == True:
			if samples[i] < 0.99:
				wetGrass = True
		elif sprinkling == True and raining == False:
			if samples[i] < 0.9:
				wetGrass = True
		elif sprinkling == False and raining == True:
			if samples[i] < 0.9:
				wetGrass = True
		sample1.append([cloudy, sprinkling, raining, wetGrass])
		cloudy = False
		sprinkling = False
		raining = False
		wetGrass = False
		i = i + 1
	return sample1

def Problem1Calc(sampleSets):
	cloudCount1 = 0
	cloudCount2 = 0
	sprinklerCount1 = 0
	sprinklerCount2 = 0
	total1 = 0
	total2 = 0
	total3 = 0
	total4 = 0
	for sample in sampleSets:
		if sample[0] == True:
			cloudCount1 = cloudCount1 + 1.0
		total1 = total1 + 1.0
		if sample[2] == True:
			if sample[0] == True:
				cloudCount2 = cloudCount2 + 1.0
			total2 = total2 + 1.0
		if sample[3] == True:
			if sample[1] == True:
				sprinklerCount1 = sprinklerCount1 + 1.0
			total3 = total3 + 1.0
		if sample[0] == True and sample[3] == True:
			if sample[1] == True:
				sprinklerCount2 = sprinklerCount2 + 1.0
			total4 = total4 + 1.0
	print"1a) P(c=true):", cloudCount1/total1
	print"1b) P(c=true|r=true):", cloudCount2/total2
	print"1c) P(s=true|w=true):", sprinklerCount1/total3
	print"1d) P(s=true|c=true,w=true):", sprinklerCount2/total4
	

# Create main function to run program
def main():
	network = createNetwork()
	question1 = Problem1()
	Problem1Calc(question1)
	
	
		
			
		

if __name__ == "__main__":
    main()


	
	
	
	
	
	
	
	
	
	
