# Assignment 8 - Hidden Markov Models
This repositiory contains Assignment 8 for CSCI 3202 - Artificial Intelligence. This assignment focuses on using Hidden Markov Models to discover typos in a text document. It also uses Viterbi probability calculations to reconstruct the expected text using the incorrect text given. It then compares this corrected text with the real text to calculate the error in the Viterbi probability calculation

#### Running The Code
To run this code, simply run the command ```$ python HiddenMarkov.py``` in the command line. 

#### Expected Output
This program will output two files:
- ```outputFile1.txt``` contains the emission probabilities and the transition probabilities for all states.
- ```outputFile2.txt``` contains the Viterbi-created text and the error rate of the Viterbi calculations.
