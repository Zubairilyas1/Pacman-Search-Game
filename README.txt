Pacman Search Project - AI Assignment 01
=========================================
Student: 24i-3142
Course: Artificial Intelligence (AI2002)
Python Version: 3.12.10

RUN COMMANDS:
=============
# Task 1: Depth-First Search (DFS)
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

# Task 2: Breadth-First Search (BFS)
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

# Task 3: Uniform-Cost Search (UCS)
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs

# Task 4: Greedy Best-First Search (GBFS)
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

# Task 5: A* Search
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

# Task 6: Corners Problem
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5

# Task 7: Food Search
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent

# Custom Maze (24i-3142Search) - all 5 algorithms:
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=dfs
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=bfs
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=ucs
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

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
- layouts/24i-3142Search.lay: Custom maze (20x17, single food dot)
- csv_logger.py: CSV trace logging utility

EVIDENCE:
=========
CSV trace logs in evidence/ directory for all algorithm runs.
Screenshots in evidence/screenshots/ directory.

