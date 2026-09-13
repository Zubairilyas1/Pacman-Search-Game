"""
CSV Trace Logger for Pacman Search Algorithms
Logs every iteration with all required columns for evidence/ directory.
"""

import csv
import os
from typing import Any, List, Optional, Set, Tuple
from datetime import datetime


class CSVLogger:
    """
    Logs search algorithm execution trace to CSV.
    
    Mandatory columns:
    iteration, expanded_state, parent, action, generated_successors,
    frontier_before, frontier_after, explored, g, h, f
    """
    
    def __init__(self, algorithm_name: str, problem_name: str, layout_name: str = "unknown"):
        self.algorithm_name = algorithm_name
        self.problem_name = problem_name
        self.layout_name = layout_name
        self.iteration = 0
        self.rows: List[dict] = []
        
        # Ensure evidence directory exists
        os.makedirs("evidence", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"evidence/{algorithm_name}_{problem_name}_{layout_name}_{timestamp}.csv"
        
        # CSV header
        self.fieldnames = [
            "iteration",
            "expanded_state",
            "parent",
            "action",
            "generated_successors",
            "frontier_before",
            "frontier_after",
            "explored",
            "g",
            "h",
            "f"
        ]
    
    def log_iteration(
        self,
        expanded_state: Any,
        parent: Any,
        action: Optional[str],
        generated_successors: List[Tuple[Any, str, float]],
        frontier_before: List[Any],
        frontier_after: List[Any],
        explored: Set[Any],
        g: float,
        h: float,
        f: float
    ) -> None:
        """Log a single search iteration."""
        self.iteration += 1
        
        def format_state(state: Any) -> str:
            if state is None:
                return "None"
            if isinstance(state, tuple):
                return str(state)
            return str(state)
        
        def format_successors(successors: List[Tuple[Any, str, float]]) -> str:
            if not successors:
                return "[]"
            return ";".join(f"({format_state(s)},{a},{c})" for s, a, c in successors)
        
        def format_frontier(frontier: List[Any]) -> str:
            if not frontier:
                return "[]"
            return ";".join(format_state(item) for item in frontier)
        
        def format_explored(explored_set: Set[Any]) -> str:
            if not explored_set:
                return "[]"
            return ";".join(format_state(s) for s in sorted(explored_set, key=str))
        
        row = {
            "iteration": self.iteration,
            "expanded_state": format_state(expanded_state),
            "parent": format_state(parent),
            "action": action if action else "START",
            "generated_successors": format_successors(generated_successors),
            "frontier_before": format_frontier(frontier_before),
            "frontier_after": format_frontier(frontier_after),
            "explored": format_explored(explored),
            "g": g,
            "h": h,
            "f": f
        }
        self.rows.append(row)
    
    def save(self) -> str:
        """Write all logged rows to CSV file."""
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)
        return self.filename
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


def create_logger(algorithm_name: str, problem_name: str, layout_name: str = "unknown") -> CSVLogger:
    """Factory function to create a CSVLogger with standardized naming."""
    return CSVLogger(algorithm_name, problem_name, layout_name)