# Jessica Petty
# CSCI 3202
# Assignment 7
# November 4, 2015

import sys

# Hard code sample data into program
samples = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28, 1, 0.95, 0.71, 0.14, 0.1, 1.0, \
	0.71, 0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97, 0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, \
	0.14, 0.13, 0.4, 0.94, 0.19, 0.6, 0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, \
	0.11, 0.83, 0.96, 0.41, 0.65, 0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97, 0.95, 0.01, 0.62, 0.32, \
	0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79, 0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

# Function to create samples from the data set for Problem 1
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

# Function to calculate the probabilities in question 1 based on the sample
def Problem1Sample(sampleSets):
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

# Function to create samples from the data set for problem 3
def Problem3():
	i = 0
	sampleSize = len(samples)
	cloudy = False
	sprinkling = False
	raining = False
	wetGrass = False
	sample3a = []
	sample3b = []
	sample3c = []
	sample3d = []
	# while loop to create samples for 3a
	while i < sampleSize:
		if samples[i] < 0.5:
			cloudy = True
		i = i + 1
		sample3a.append([cloudy, sprinkling, raining, wetGrass])
		cloudy = False
	# while loop to create samples for 3b
	i = 0
	while i < sampleSize:
		if samples[i] < 0.5:
			cloudy = True
		i = i + 1
		if cloudy == True:
			if samples[i] < 0.8:
				raining = True
				i = i + 1
				sample3b.append([cloudy, sprinkling, raining, wetGrass])
			else:
				i = i + 1
		else:
			if samples[i] < 0.2:
				raining = True
				i = i + 1
				sample3b.append([cloudy, sprinkling, raining, wetGrass])
			else:
				i = i + 1
		cloudy = False
		raining = False
	# while loop to create samples for 3c
	i = 0
	while i < sampleSize:
		if samples[i] < 0.5:
			cloudy = True
		i = i + 1
		if cloudy == True:
			if samples[i] < 0.1:
				sprinkling = True
			i = i + 1
			if samples[i] < 0.8:
				raining = True
			i = i + 1
		else:
			if samples[i] < 0.5:
				sprinkling = True
			i = i + 1
			if samples[i] < 0.2:
				raining = True
			i = i + 1
		if sprinkling == True and raining == True:
			if samples[i] < 0.99:
				sample3c.append([cloudy, sprinkling, raining, True])
		elif sprinkling == True and raining == False:
			if samples[i] < 0.9:
				sample3c.append([cloudy, sprinkling, raining, True])
		elif sprinkling == False and raining == True:
			if samples[i] < 0.9:
				sample3c.append([cloudy, sprinkling, raining, True])
		i = i + 1
		cloudy = False
		sprinkling = False
		raining = False
	# while loop to create samples for problem 3d
	i = 0 
	while i < sampleSize-3:
		if samples[i] < 0.5:
			cloudy = True
			i = i + 1
		else:
			i = i + 1
			continue
		if samples[i] < 0.1:
			sprinkling = True
		i = i + 1
		if samples[i] < 0.8:
			raining = True
		i = i + 1
		if sprinkling == True and raining == True:
			if samples[i] < 0.99:
				sample3d.append([cloudy, sprinkling, raining, True])
		elif sprinkling == True and raining == False:
			if samples[i] < 0.90:
				sample3d.append([cloudy, sprinkling, raining, True])
		elif sprinkling == False and raining == True:
			if samples[i] < 0.90:
				sample3d.append([cloudy, sprinkling, raining, True])
		i = i + 1
		cloudy = False
		sprinkling = False
		raining = False
	
	# for loop to calculate the probability for problem 3a
	probCount3a = 0.0
	total3a = 0.0
	for sample in sample3a:
		if sample[0] == True:
			probCount3a = probCount3a + 1
		total3a = total3a + 1
	print"3a) P(c=true):", probCount3a/total3a
	# for loop to calculate the probability for problem 3b
	probCount3b = 0.0
	total3b = 0.0
	for sample in sample3b:
		if sample[0] == True:
			probCount3b = probCount3b + 1
		total3b = total3b + 1
	print"3b) P(c=true|r=true):", probCount3b/total3b
	# for loop to calculate the probability for problem3c
	probCount3c = 0.0
	total3c = 0.0
	for sample in sample3c:
		if sample[1] == True:
			probCount3c = probCount3c + 1
		total3c = total3c + 1
	print"3c) P(s=true|w=true):", probCount3c/total3c
	# for loop to calculate the probability for problem3d
	probCount3d = 0.0
	total3d = 0.0
	for sample in sample3d:
		if sample[1] == True:
			probCount3d = probCount3d + 1
		total3d = total3d + 1
	print"3d) P(s=true|c=true,w=true):", probCount3d/total3d
	
# Create main function to run program
def main():
	question1 = Problem1()
	Problem1Sample(question1)
	Problem3()		

if __name__ == "__main__":
    main()
