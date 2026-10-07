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


def _get_layout_name(problem):
    """
    Extract a human-readable layout identifier from the problem.
    Uses the stored _layout_name attribute if available (set by searchAgents),
    otherwise falls back to maze dimensions as a unique-enough identifier.
    """
    # First try: explicit layout name set by the problem (best case)
    name = getattr(problem, '_layout_name', None)
    if name:
        return name
    # Second try: derive from walls dimensions (e.g. "36x18")
    walls = getattr(problem, 'walls', None)
    if walls is not None:
        try:
            return "{}x{}".format(walls.width, walls.height)
        except Exception:
            pass
    return "unknown"


def _graph_search(problem, fringe, heuristic=None, algorithm_name="search",
                  problem_name="SearchProblem", layout_name="unknown"):
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

    # Fringe stores tuples: (state, actions_list, path_cost, parent_state, action_taken)
    if hasattr(fringe, 'heap'):  # PriorityQueue (UCS, A*, GBFS)
        fringe.push((start_state, [], 0, None, "START"), start_h)
    else:  # Stack (DFS) or Queue (BFS)
        fringe.push((start_state, [], 0, None, "START"))

    explored = set()

    while not fringe.isEmpty():

        # Capture frontier BEFORE pop for this iteration's log
        if hasattr(fringe, 'heap'):
            frontier_before = [item[2][0] for item in fringe.heap]
        elif hasattr(fringe, 'list'):
            frontier_before = [item[0] for item in fringe.list]
        else:
            frontier_before = []

        # Pop the next node from the fringe
        state, actions, path_cost, parent_state, action_taken = fringe.pop()

        # Goal test at dequeue (required for UCS/A* optimality guarantee)
        if problem.isGoalState(state):
            logger.log_iteration(
                expanded_state=state,
                parent=parent_state,
                action=action_taken if action_taken != "START" else "GOAL",
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

        # Skip states already fully expanded
        if state in explored:
            continue

        # Get successors (N->E->S->W expansion order as required by assignment)
        successors = problem.getSuccessors(state)

        # Compute g, h, f values for this node
        g = path_cost
        h = heuristic(state, problem) if heuristic else 0
        f = g + h

        # Mark state as explored BEFORE pushing successors
        explored.add(state)

        # Build O(1) frontier set for BFS duplicate detection (Fix: was O(n) scan)
        frontier_set = set()
        if type(fringe).__name__ == 'Queue':
            frontier_set = {item[0] for item in fringe.list}

        # Push successors to fringe FIRST — frontier_after captured AFTER this loop
        for successor, action, step_cost in successors:
            if successor in explored:
                continue

            new_cost = path_cost + step_cost
            new_actions = actions + [action]

            # BFS: skip if successor already queued in the frontier (O(1) check)
            if type(fringe).__name__ == 'Queue':
                if successor in frontier_set:
                    continue
                frontier_set.add(successor)

            # Compute priority for informed searches
            if algorithm_name == "gbfs":
                priority = heuristic(successor, problem) if heuristic else 0
            elif heuristic:
                priority = new_cost + heuristic(successor, problem)
            else:
                priority = new_cost

            if hasattr(fringe, 'heap'):  # PriorityQueue (UCS, A*, GBFS)
                # update() re-prioritizes if successor already in frontier with higher cost
                # Satisfies assignment: "update its priority in the queue"
                fringe.update((successor, new_actions, new_cost, state, action), priority)
            else:  # Stack (DFS) or Queue (BFS)
                fringe.push((successor, new_actions, new_cost, state, action))

        # Capture frontier_after NOW - correctly AFTER all successors have been pushed
        if hasattr(fringe, 'heap'):
            frontier_after = [item[2][0] for item in fringe.heap]
        elif hasattr(fringe, 'list'):
            frontier_after = [item[0] for item in fringe.list]
        else:
            frontier_after = []

        # Log this iteration with the correct frontier_after
        logger.log_iteration(
            expanded_state=state,
            parent=parent_state,
            action=action_taken,
            generated_successors=successors,
            frontier_before=frontier_before,
            frontier_after=frontier_after,
            explored=explored,
            g=g,
            h=h,
            f=f
        )

    logger.save()
    return None


def depthFirstSearch(problem):
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
    fringe = util.Stack()
    return _graph_search(
        problem, fringe,
        algorithm_name="dfs",
        problem_name=problem.__class__.__name__,
        layout_name=_get_layout_name(problem)
    )


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fringe = util.Queue()
    return _graph_search(
        problem, fringe,
        algorithm_name="bfs",
        problem_name=problem.__class__.__name__,
        layout_name=_get_layout_name(problem)
    )


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        algorithm_name="ucs",
        problem_name=problem.__class__.__name__,
        layout_name=_get_layout_name(problem)
    )


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    """Search the node with lowest heuristic value first."""
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        heuristic=heuristic,
        algorithm_name="gbfs",
        problem_name=problem.__class__.__name__,
        layout_name=_get_layout_name(problem)
    )


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    fringe = util.PriorityQueue()
    return _graph_search(
        problem, fringe,
        heuristic=heuristic,
        algorithm_name="astar",
        problem_name=problem.__class__.__name__,
        layout_name=_get_layout_name(problem)
    )


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
