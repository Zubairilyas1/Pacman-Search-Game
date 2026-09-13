# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from typing import Any, Callable, List, Optional, Set, Tuple
from csv_logger import create_logger


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def _graph_search(
    problem: SearchProblem,
    fringe: Any,
    heuristic: Callable = None,
    algorithm_name: str = "search",
    problem_name: str = "SearchProblem",
    layout_name: str = "unknown"
) -> Optional[List[str]]:
    """
    Generic graph search with CSV trace logging.
    
    Args:
        problem: SearchProblem instance
        fringe: util.Stack, util.Queue, or util.PriorityQueue
        heuristic: heuristic function for A*/GBFS, None for DFS/BFS/UCS
        algorithm_name: name for CSV logging
        problem_name: problem class name for CSV logging
        layout_name: layout name for CSV logging
    
    Returns:
        List of actions to reach goal, or None if no solution
    """
    logger = create_logger(algorithm_name, problem_name, layout_name)
    
    start_state = problem.getStartState()
    start_h = heuristic(start_state, problem) if heuristic else 0
    start_f = start_h
    
    # Fringe stores tuples: (state, actions_list, path_cost)
    # For priority queue: (priority, (state, actions_list, path_cost))
    if hasattr(fringe, 'push') and hasattr(fringe, 'pop'):
        if hasattr(fringe, 'heap'):  # PriorityQueue
            fringe.push((start_state, [], 0), start_f)
        else:  # Stack or Queue
            fringe.push((start_state, [], 0))
    
    explored: Set[Any] = set()
    iteration = 0
    
    while not fringe.isEmpty():
        iteration += 1
        
        # Get current frontier state for logging (before pop)
        if hasattr(fringe, 'heap'):
            frontier_before = [item[2][0] for item in fringe.heap]
        elif hasattr(fringe, 'list'):
            frontier_before = [item[0] for item in fringe.list]
        else:
            frontier_before = []
        
        # Pop from fringe
        if hasattr(fringe, 'heap'):  # PriorityQueue
            current = fringe.pop()
            state, actions, path_cost = current
        else:  # Stack or Queue
            state, actions, path_cost = fringe.pop()
        
        # Check if goal
        if problem.isGoalState(state):
            # Log final iteration
            logger.log_iteration(
                expanded_state=state,
                parent=actions[-1] if actions else None,
                action=actions[-1] if actions else "GOAL",
                generated_successors=[],
                frontier_before=frontier_before,
                frontier_after=[],
                explored=explored,
                g=path_cost,
                h=0,
                f=path_cost
            )
            logger.save()
            return actions
        
        # Skip if already explored
        if state in explored:
            continue
        
        # Mark as explored
        explored.add(state)
        
        # Get successors (N->E->S->W order as required)
        successors = problem.getSuccessors(state)
        
        # Log this iteration
        g = path_cost
        h = heuristic(state, problem) if heuristic else 0
        f = g + h
        
        # Generate frontier after adding successors
        if hasattr(fringe, 'heap'):
            frontier_after = [item[2][0] for item in fringe.heap]
        elif hasattr(fringe, 'list'):
            frontier_after = [item[0] for item in fringe.list]
        else:
            frontier_after = []
        
        logger.log_iteration(
            expanded_state=state,
            parent=actions[-1] if actions else None,
            action=actions[-1] if actions else "START",
            generated_successors=successors,
            frontier_before=frontier_before,
            frontier_after=frontier_after,
            explored=explored.copy(),
            g=g,
            h=h,
            f=f
        )
        
        # Add successors to fringe
        for successor, action, step_cost in successors:
            if successor not in explored:
                new_actions = actions + [action]
                new_cost = path_cost + step_cost
                
                if heuristic:
                    priority = new_cost + heuristic(successor, problem)
                else:
                    priority = new_cost
                
                if hasattr(fringe, 'heap'):  # PriorityQueue
                    # Check if already in fringe with higher cost
                    fringe.update((successor, new_actions, new_cost), priority)
                else:  # Stack or Queue
                    fringe.push((successor, new_actions, new_cost))
    
    logger.save()
    return None


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    from searchAgents import PositionSearchProblem
    layout_name = "unknown"
    if isinstance(problem, PositionSearchProblem):
        layout_name = getattr(problem, '_layout_name', 'unknown')
    
    fringe = util.Stack()
    return _graph_search(
        problem, fringe,
        algorithm_name="dfs",
        problem_name=problem.__class__.__name__,
        layout_name=layout_name
    )


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    from searchAgents import PositionSearchProblem
    layout_name = "unknown"
    if isinstance(problem, PositionSearchProblem):
        layout_name = getattr(problem, '_layout_name', 'unknown')
    
    fringe = util.Queue()
    return _graph_search(
        problem, fringe,
        algorithm_name="bfs",
        problem_name=problem.__class__.__name__,
        layout_name=layout_name
    )


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    from searchAgents import PositionSearchProblem
    layout_name = "unknown"
    if isinstance(problem, PositionSearchProblem):
        layout_name = getattr(problem, '_layout_name', 'unknown')
    
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        algorithm_name="ucs",
        problem_name=problem.__class__.__name__,
        layout_name=layout_name
    )


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node with lowest heuristic value first."""
    from searchAgents import PositionSearchProblem
    layout_name = "unknown"
    if isinstance(problem, PositionSearchProblem):
        layout_name = getattr(problem, '_layout_name', 'unknown')
    
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        heuristic=heuristic,
        algorithm_name="gbfs",
        problem_name=problem.__class__.__name__,
        layout_name=layout_name
    )


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from searchAgents import PositionSearchProblem
    layout_name = "unknown"
    if isinstance(problem, PositionSearchProblem):
        layout_name = getattr(problem, '_layout_name', 'unknown')
    
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        heuristic=heuristic,
        algorithm_name="astar",
        problem_name=problem.__class__.__name__,
        layout_name=layout_name
    )


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch