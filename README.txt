Pacman Search Project - AI Assignment 01
=========================================
Student: 24i-3142
Course: Artificial Intelligence (AI2002)
Python Version: 3.12.10

RUN COMMANDS:
=============
# Core algorithms on standard mazes
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

# Multi-goal problems
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent

# Custom maze
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=bfs

# Run all autograder tests
python autograder.py

SYSTEM SPECS:
=============
OS: Windows 11
Python: 3.12.10
CPU: Intel Core i7
RAM: 16GB

FILES MODIFIED:
===============
- search.py: DFS, BFS, UCS, GBFS, A* with CSV logging
- searchAgents.py: CornersProblem, cornersHeuristic, foodHeuristic, AnyFoodSearchProblem, ClosestDotSearchAgent
- layouts/24i-3142Search.lay: Custom maze
- csv_logger.py: CSV trace logging utility

EVIDENCE:
=========
CSV trace logs in evidence/ directory for all algorithm runs