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

# Fetch arguments, options from command line
opts, args = getopt.getopt(sys.argv[1:], 'm:j:p:g')
# Evaluate options, call appropriate function
for opt in opts:
	if opt[0] == '-m':
		arg = opt[1]
		# call marginal probability function
	elif opt[0] == '-j':
		arg = opt[1]
		# call joint probability function
	elif opt[0] == '-p':
		arg = opt[1]
		probability = sys.argv[2]
		# call set prior function for smoking or pollution
	elif opt[0] == '-g':
		arg = opt[1]
		# call conditional probability function

# Function to parse the argument from option list
def parseArgument(arg):
	# Parse the argument 
	print(arg)
