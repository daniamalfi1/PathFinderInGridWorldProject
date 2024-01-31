# PathFinderInGridWorldProject
Project for introduction to artificial intelligence course at University of North Florida. Implementation of a path finding agent traveling from point to point in a two-dimensional grid world using 4 different graph search algorithms.
Some of the files were provided. In Project 2 pdf file the project description along with the provided files and the implementation requirements is included. 

Project 2: Path Finder in Grid World
Daniela Amalfi Ojeda
Course: Introduction to Artificial Intelligence, UNF
The following program implements four different search algorithms to find the path from a source to a destination. The source and the destinations are explicitally defined in the code and to change it, it needs to be changed in the code. To run the code the search.py program needs to be run and it will automatically run all four search algorithms in the following order: breadth-first search (BFS), 
depth-first search (DFS), greedy best-first search (GBFS), and A* search. In the command line a summary for each algorithm will be included. The summary displays the number of nodes expanded and the path cost for each algorithm. Additionally a plot will be shown with the path of each algorithm represented in a different color. BFS will be first displayed in red, DFS will then be displayed in yellow, GBFS will be displayed in orange and finally A* will be displayed in blue. To run the code there are some libraries that need to be included:

import math
from matplotlib.path import Path
import matplotlib.pyplot as plt
import heapq

In the Project2 file a TestingGrid folder contains the coordinates for the turf and enclosures created by the student. The folder also contains images with the examples of the search algorithms on this new grid.

COMMENTS: All of the search files are implemented in the code, but the A* does not return the expected path for the given testingGrid.
