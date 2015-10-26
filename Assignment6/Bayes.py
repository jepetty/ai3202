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

