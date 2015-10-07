This repository is Assignment 5 for CSCI 3202 Artificial Intelligence.
This assignment focuses on Markov Decision Processes, using MDPs to navigate a maze.

Question: Can you find values of epsilon to change the path your program finds?

Yes. I tried values between 0 and 40 (40 being around the maximum initial change in utility for the nodes in the graph). For values less than 0.5 (all the way to as small as 0.001), there was no change in the path of the solution, and little change in the utilities found. But, for larger values (those greater than 30), the actual path of my solution changed, and the utilities it generated were much smaller. This shows that the smaller the allowable error, the more optimal the path becomes (to a certain extent).
