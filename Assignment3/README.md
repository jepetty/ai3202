Repository for Assignment 2 for CSCI 3202 - Artificial Intelligence. This assignment focuses on implementing AStarSearch and using and creating heuristics.
test
Heuristic 1:
The Manhattan distance is found by adding the change in x-distance between two points and the change in y-distance between those points. ie:
distMan = |x2-x1| + |y2-y1|

Heuristic 2:
The Euclidean distance is found by finding the straightline distance between your point and the destination using Pythagorean's Theorem. ie:
distEuc = sqrt((x2-x1)^2 + (y2-y1)^2)

I liked the Euclidean distance as a heuristic because the diagonal route to the solution will be the most cost-efficient solution, so I thought this heuristic (because it is diagonal-focused), would keep our solution trending towards the diagonal, and would thus be most cost efficient.

As seen from the analysis of the first world, the Euclidean distance does take a more diagonally-centric path from start to the end node. It also has a better overall cost and node count, with a cost of 138 (compared to 156 for the Manhattan distance) and a node count of only 12 (compared to 13 for the Manhattan distance). For the second world, no difference was seen between the output of the Euclidean distance heuristic and the Manhattan distance heuristic.
