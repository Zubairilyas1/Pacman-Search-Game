# Pacman Search Project - Complete Demo & Run Guide
## AI Assignment 01 (AI2002) | Student: 24i-3142

---

## 📋 TABLE OF CONTENTS
1. [Environment Setup](#1-environment-setup)
2. [Project Structure](#2-project-structure)
3. [Core Algorithm Demos (Tasks 1-5)](#3-core-algorithm-demos-tasks-1-5)
4. [Multi-Goal Search Demos (Tasks 6-8)](#4-multi-goal-search-demos-tasks-6-8)
5. [Custom Maze Demo](#5-custom-maze-demo)
6. [Autograder Test Suite](#6-autograder-test-suite)
7. [CSV Trace Logging Evidence](#7-csv-trace-logging-evidence)
8. [Key Code Walkthrough](#8-key-code-walkthrough)
9. [Viva Presentation Script](#9-viva-presentation-script)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. ENVIRONMENT SETUP

### 1.1 Prerequisites
```bash
# Python 3.7+ required (tested on 3.12.10)
python --version
# Python 3.12.10

# Verify project structure
ls search/
# Should show: pacman.py, game.py, util.py, search.py, searchAgents.py, layouts/, test_cases/, evidence/
```

### 1.2 Quick Sanity Check
```bash
cd search
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
# Expected: "Path found with total cost of 10" + "Pacman emerges victorious!"
```

---

## 2. PROJECT STRUCTURE

```
search/
├── MODIFIED FILES (Required by Assignment)
│   ├── search.py              # DFS, BFS, UCS, GBFS, A* + CSV logging
│   ├── searchAgents.py        # CornersProblem, FoodSearch, heuristics
│   ├── csv_logger.py          # CSV trace logger utility
│   └── layouts/24i-3142Search.lay  # Custom maze
│
├── ORIGINAL FILES (DO NOT MODIFY)
│   ├── pacman.py              # Game loop, CLI parser
│   ├── game.py                # GameState, Directions, Grid
│   ├── util.py                # Stack, Queue, PriorityQueue
│   ├── layout.py              # Layout loader
│   ├── graphicsDisplay.py     # GUI rendering
│   ├── graphicsUtils.py
│   ├── textDisplay.py
│   └── ... (other support files)
│
├── TEST CASES
│   └── test_cases/q1-q8/      # Autograder test cases
│
├── EVIDENCE (Auto-generated)
│   └── evidence/*.csv         # Trace logs per algorithm run
│
└── DOCUMENTATION
    ├── README.txt             # Run commands & system specs
    ├── plan.md                # Implementation plan
    ├── report.md              # Full analysis report
    └── .gitignore             # Ignores large CSVs, cache
```

---

## 3. CORE ALGORITHM DEMOS (TASKS 1-5)

### 3.1 Task 1: Depth-First Search (DFS)
```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs
```

**Expected Output (mediumMaze):**
```
[SearchAgent] using function dfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 130 in 0.0 seconds
Search nodes expanded: 146
Pacman emerges victorious! Score: 380
```

**Key Points to Demo:**
- Uses `util.Stack` (LIFO)
- Graph search: maintains `explored` set
- Expansion order: **North → East → South → West**
- Non-optimal path (130 vs BFS's 68)

---

### 3.2 Task 2: Breadth-First Search (BFS)
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs
```

**Expected Output (mediumMaze):**
```
[SearchAgent] using function bfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 269
Pacman emerges victorious! Score: 442
```

**Key Points to Demo:**
- Uses `util.Queue` (FIFO)
- Graph search: checks both `explored` AND `frontier`
- **Guarantees optimal path** for unweighted graphs
- More nodes expanded than DFS (269 vs 146)

---

### 3.3 Task 3: Uniform-Cost Search (UCS)
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p SearchAgent -a fn=ucs
# If stayEastSearch layout exists:
python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs
```

**Expected Output (mediumMaze):**
```
[SearchAgent] using function ucs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.1 seconds
Search nodes expanded: 269
```

**Key Points to Demo:**
- Uses `util.PriorityQueue` ordered by **g(n) = path cost**
- `fringe.update()` handles cheaper paths to same state
- Same as BFS when all costs = 1
- **Handles weighted edges** (e.g., stayEastSearch: cost = 0.5^x)

---

### 3.4 Task 4: Greedy Best-First Search (GBFS)
```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
```

**Expected Output:**
```
[SearchAgent] using function gbfs and heuristic manhattanHeuristic
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 210 in 0.2 seconds
Search nodes expanded: 549
```

**Key Points to Demo:**
- Priority queue ordered by **h(n) only** (heuristic)
- **CLI heuristic parameter**: `heuristic=manhattanHeuristic`
- Also supports: `heuristic=euclideanHeuristic`
- **NOT optimal** - can get trapped by local minima

---

### 3.5 Task 5: A* Search
```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

**Expected Output (with Manhattan):**
```
[SearchAgent] using function astar and heuristic manhattanHeuristic
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 210 in 0.2 seconds
Search nodes expanded: 549
```

**Key Points to Demo:**
- Priority queue ordered by **f(n) = g(n) + h(n)**
- **Optimal** with admissible, consistent heuristic
- Manhattan heuristic is both admissible & consistent
- Fewer nodes than BFS when heuristic is informed

---

### 3.6 Algorithm Comparison Summary (Run All)
```bash
# Quick comparison on mediumMaze
echo "=== DFS ===" && python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs 2>&1 | tail -3
echo "=== BFS ===" && python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs 2>&1 | tail -3
echo "=== UCS ===" && python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs 2>&1 | tail -3
echo "=== A* (Manhattan) ===" && python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic 2>&1 | tail -3
```

**Expected Results Table:**
| Algorithm | Path Cost | Nodes Expanded | Optimal? |
|-----------|-----------|----------------|----------|
| DFS       | 130       | 146            | ❌       |
| BFS       | 68        | 269            | ✅       |
| UCS       | 68        | 269            | ✅       |
| A* (Manhattan) | 68   | 221            | ✅       |

---

## 4. MULTI-GOAL SEARCH DEMOS (TASKS 6-8)

### 4.1 Task 6: CornersProblem
```bash
# BFS on tinyCorners (exact solution required)
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem

# A* with custom heuristic on mediumCorners
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5
```

**Expected Output (mediumCorners):**
```
Path found with total cost of 106 in 0.8 seconds
Search nodes expanded: 774
Pacman emerges victorious! Score: 434
```

**State Representation to Explain:**
```python
# In searchAgents.py CornersProblem:
def getStartState(self):
    visited = tuple([False] * 4)  # 4 corners
    return (self.startingPosition, visited)

def isGoalState(self, state):
    position, visited = state
    return all(visited)  # All 4 corners visited
```

**Heuristic: `cornersHeuristic` (MST over unvisited corners)**
```python
def cornersHeuristic(state, problem):
    position, visited = state
    unvisited = [c for i,c in enumerate(corners) if not visited[i]]
    min_dist = min(manhattanDistance(position, c) for c in unvisited)
    mst_cost = MST(unvisited)  # Prim's algorithm with Manhattan distance
    return min_dist + mst_cost
```

---

### 4.2 Task 7: Food Search Problem (A* + MST Heuristic)
```bash
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

**Expected Output:**
```
Path found with total cost of 60 in 6.9 seconds
Search nodes expanded: 2012
Pacman emerges victorious! Score: 570
```

**⚡ KEY ACHIEVEMENT: 2012 nodes < 7000 threshold = BONUS 5/4 marks**

**State Representation:**
```python
# State = (pacmanPosition, foodGrid)
# foodGrid = Grid of True/False (True = food present)
```

**Heuristic: `foodHeuristic` (Precomputed Maze Distance MST)**
```python
def foodHeuristic(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()
    
    # Precompute ONCE: all-pairs maze distances between food dots
    if 'maze_distances' not in problem.heuristicInfo:
        for f1, f2 in combinations(all_food, 2):
            maze_dists[(f1,f2)] = len(bfs(PositionSearchProblem(start=f1, goal=f2)))
    
    # MST over REMAINING food using TRUE maze distances
    min_dist = min(mazeDistance(position, f) for f in foodList)
    mst_cost = MST(remaining_food, maze_dists)
    return min_dist + mst_cost
```

**Why This Works:**
- Manhattan distance underestimates by **5-13x** in trickySearch
- Precomputes exact maze distances once, then MST is fast
- Caches results per food configuration

---

### 4.3 Task 8: Closest Dot Search Agent
```bash
python pacman.py -l bigSearch -p ClosestDotSearchAgent
```

**Expected Output:**
```
[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with cost 350.
Pacman emerges victorious! Score: 2360
```

**Implementation:**
```python
class AnyFoodSearchProblem(PositionSearchProblem):
    def isGoalState(self, state):
        x, y = state
        return self.food[x][y]  # Goal = ANY food dot

class ClosestDotSearchAgent(SearchAgent):
    def findPathToClosestDot(self, gameState):
        problem = AnyFoodSearchProblem(gameState)
        return search.bfs(problem)  # BFS finds closest in unweighted graph
```

**Strategy:** Repeatedly finds closest dot → eats it → repeats until all food gone.

---

## 5. CUSTOM MAZE DEMO

### 5.1 Custom Layout: `24i-3142Search.lay`
```bash
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=bfs
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
```

**Layout Features:**
- **Size:** 16×25, 30 food dots
- **Multiple branches** forcing exploration
- **Dead ends** that trap GBFS (greedy)
- **Deceptive corridors** where A* excels with heuristic
- **Symmetric design** for visual comparison

---

## 6. AUTOGRADER TEST SUITE

### 6.1 Run All Tests
```bash
cd search
python autograder.py
```

### 6.2 Expected Results
```
Question q1: 3/3  (DFS)
Question q2: 3/3  (BFS)
Question q3: 3/3  (UCS)
Question q4: 3/3  (A*)
Question q5: 3/3  (Corners BFS)
Question q6: 3/3  (Corners A*)
Question q7: 5/4  (Food Search - BONUS!)
Question q8: 3/3  (Closest Dot)
------------------
Total: 26/25
```

### 6.3 Run Individual Questions
```bash
python autograder.py -q q1    # DFS only
python autograder.py -q q3    # UCS only
python autograder.py -q q6    # Corners A* only
python autograder.py -q q7    # Food Search only
```

---

## 7. CSV TRACE LOGGING EVIDENCE

### 7.1 Location & Format
```bash
ls search/evidence/
# Contains: *_PositionSearchProblem_*.csv, *_CornersProblem_*.csv, etc.
```

### 7.2 CSV Columns (All 11 Required)
```csv
iteration,expanded_state,parent,action,generated_successors,frontier_before,frontier_after,explored,g,h,f
```

### 7.3 Sample CSV Content (First 3 lines)
```csv
iteration,expanded_state,parent,action,generated_successors,frontier_before,frontier_after,explored,g,h,f
1,"(5, 5)",None,START,"((5, 4),South,1);((4, 5),West,1)",[],"(5, 4);(4, 5)",[],0,0,0
2,"(4, 5)","(5, 5)",West,"((5, 5),East,1);((3, 5),West,1)","(5, 4);(4, 5)","(5, 4)","(4, 5);(5, 5)",1,0,1
3,"(3, 5)","(4, 5)",West,"((4, 5),East,1);((2, 5),West,1)","(5, 4);(3, 5)","(5, 4)","(3, 5);(4, 5);(5, 5)",2,0,2
```

### 7.4 Verify Logging Works
```bash
# Run any algorithm, then check evidence/
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
ls search/evidence/dfs_PositionSearchProblem_*.csv
head -5 search/evidence/dfs_PositionSearchProblem_*.csv
```

---

## 8. KEY CODE WALKTHROUGH

### 8.1 `search.py` - Core Algorithms
```python
# Shared graph search with CSV logging (lines 69-200)
def _graph_search(problem, fringe, heuristic=None, algorithm_name="search", ...):
    logger = create_logger(algorithm_name, problem_name, layout_name)
    
    # Initialize fringe with start state
    # Loop: pop, check goal, expand, log, push successors
    # Returns action list or None

# Algorithm entry points (all call _graph_search)
def depthFirstSearch(problem):
    return _graph_search(problem, util.Stack(), algorithm_name="dfs", ...)

def breadthFirstSearch(problem):
    return _graph_search(problem, util.Queue(), algorithm_name="bfs", ...)

def uniformCostSearch(problem):
    return _graph_search(problem, util.PriorityQueue(), algorithm_name="ucs", ...)

def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    return _graph_search(problem, util.PriorityQueue(), heuristic=heuristic, algorithm_name="gbfs", ...)

def aStarSearch(problem, heuristic=nullHeuristic):
    return _graph_search(problem, util.PriorityQueue(), heuristic=heuristic, algorithm_name="astar", ...)
```

### 8.2 `searchAgents.py` - Multi-Goal Problems

**CornersProblem (lines 263-334):**
```python
class CornersProblem(search.SearchProblem):
    def getStartState(self):
        return (self.startingPosition, (False, False, False, False))
    
    def getSuccessors(self, state):
        position, visited = state
        for action in [NORTH, SOUTH, EAST, WEST]:
            nextPos = ...
            if not wall:
                nextVisited = list(visited)
                if nextPos in self.corners: nextVisited[corner_idx] = True
                successors.append(((nextPos, tuple(nextVisited)), action, 1))
```

**CornersHeuristic (lines 337-380):**
```python
def cornersHeuristic(state, problem):
    position, visited = state
    unvisited = [c for i,c in enumerate(corners) if not visited[i]]
    min_dist = min(manhattanDistance(position, c) for c in unvisited)
    mst_cost = prim_mst(unvisited, manhattanDistance)  # Admissible
    return min_dist + mst_cost
```

**FoodHeuristic (lines 452-580):**
```python
def foodHeuristic(state, problem):
    # Precompute maze distances ONCE
    if 'maze_distances' not in problem.heuristicInfo:
        for f1, f2 in combinations(all_food, 2):
            prob = PositionSearchProblem(start=f1, goal=f2)
            maze_dists[(f1,f2)] = len(bfs(prob))
    
    # MST over remaining food with TRUE maze distances
    return min_maze_dist + mst_cost
```

---

## 9. VIVA PRESENTATION SCRIPT

### 9.1 Opening (2 min)
> "I implemented all 5 search algorithms plus 3 multi-goal problems. All 8 autograder tests pass with 26/25 marks including bonus on food search."

### 9.2 Core Algorithms Demo (5 min)
| Demo | Command | Talking Point |
|------|---------|---------------|
| DFS vs BFS | `python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs` then `fn=bfs` | "DFS: 130 cost, 146 nodes. BFS: 68 cost, 269 nodes. BFS optimal for unweighted." |
| UCS weighted | `python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs` | "PriorityQueue with g(n). Updates fringe when cheaper path found." |
| GBFS vs A* | Run both on bigMaze | "GBFS: h(n) only, can get stuck. A*: f(n)=g+h, optimal with Manhattan." |

### 9.3 Multi-Goal Demo (5 min)
| Demo | Command | Talking Point |
|------|---------|---------------|
| Corners | `python pacman.py -l mediumCorners -p AStarCornersAgent -z .5` | "State = (pos, visited_4_corners). Heuristic = min_dist + MST(unvisited)." |
| Food Search | `python pacman.py -l trickySearch -p AStarFoodSearchAgent` | "**2012 nodes expanded** (threshold 7000). Precomputed maze distance MST." |
| Closest Dot | `python pacman.py -l bigSearch -p ClosestDotSearchAgent` | "Inherits PositionSearchProblem, overrides isGoalState to check food grid." |

### 9.4 Technical Deep-Dive (3 min)
> **CSV Logging:** "Every iteration logs all 11 columns. See `evidence/astar_PositionSearchProblem_*.csv`"
>
> **Heuristic Admissibility:** "Manhattan ≤ maze distance. MST over subset ≤ optimal path. Both admissible and consistent."
>
> **Code Quality:** "Shared `_graph_search()` eliminates duplication. Full type hints. No forbidden files modified."

### 9.5 Custom Maze (2 min)
> "Designed 24i-3142Search.lay with branches, dead ends, deceptive traps to show GBFS vs A* difference."

---

## 10. TROUBLESHOOTING

### 10.1 Common Issues

| Issue | Solution |
|-------|----------|
| `python` not found | Use full path: `C:\Users\Zbook\AppData\Local\Programs\Python\Python312\python.exe` |
| Layout not found | Ensure running from `search/` directory |
| "Method not implemented" | Check `search.py` / `searchAgents.py` have implementations |
| Timeout on trickySearch | Normal - takes ~7s. Increase timeout if needed. |
| Large CSV files | Ignored by `.gitignore`. Regenerate with `python autograder.py` |

### 10.2 Verify Forbidden Files Unchanged
```bash
# These should show as unmodified in git
git diff search/pacman.py
git diff search/game.py
git diff search/util.py
git diff search/layout.py
# All should show no differences
```

### 10.3 Regenerate Evidence
```bash
# Remove old evidence, run autograder to regenerate
rm search/evidence/*.csv
python autograder.py
```

---

## 📦 SUBMISSION CHECKLIST

- [ ] `search.py` - All 5 algorithms + CSV logging
- [ ] `searchAgents.py` - CornersProblem, FoodSearch, heuristics
- [ ] `csv_logger.py` - Trace logging utility
- [ ] `layouts/24i-3142Search.lay` - Custom maze
- [ ] `evidence/` - CSV logs from all runs
- [ ] `README.txt` - Run commands, system specs
- [ ] `report.md` - Full analysis (complexity, proofs, results)
- [ ] `.gitignore` - Ignores large CSVs, cache
- [ ] All autograder tests pass (26/25)

---

## 🚀 QUICK REFERENCE COMMANDS

```bash
# Core algorithms
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

# Multi-goal
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent

# Custom maze
python pacman.py -l 24i-3142Search -p SearchAgent -a fn=bfs

# Tests
python autograder.py
python autograder.py -q q7    # Specific question

# Evidence
ls search/evidence/
head search/evidence/*.csv
```

---

**Last Updated:** September 11, 2026  
**Status:** ✅ All tests passing (26/25)  
**Ready for Demo & Submission**