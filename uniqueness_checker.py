from pysat.formula import CNF
from pysat.solvers import Glucose3
from typing import Tuple, Dict, Optional, List

from count_grid_to_constraints import grid_to_constraints
from create_SAT_problem import create_multiple_eqN_constraints
from mosaic_puzzle import MosaicPuzzle

def create_blocking_clauses(var_mapping: Dict[Tuple[int, int], int], solution: List[List[bool]]) -> List[List[int]]:
    """
    Create clauses that block a specific solution.
    At least one cell must be different from the solution.
    """
    # Create one big clause: (NOT x1 OR NOT x2 ... OR NOT xn) for True cells
    # and (x1 OR x2 ... OR xn) for False cells
    blocking_clause = []
    for y in range(len(solution)):
        for x in range(len(solution[0])):
            var = var_mapping[(x, y)]
            if solution[y][x]:
                blocking_clause.append(-var)  # Must flip at least one True to False
            else:
                blocking_clause.append(var)   # Must flip at least one False to True
    return [blocking_clause]

def check_uniqueness(puzzle: MosaicPuzzle) -> Tuple[bool, Optional[List[List[bool]]]]:
    """
    Check if puzzle has a unique solution.
    Returns (is_unique, alternative_solution)
    """
    # Convert puzzle to constraints using existing function
    constraints, var_mapping = grid_to_constraints(puzzle.clues)
    
    # Create SAT encoding
    cnf_clauses, _ = create_multiple_eqN_constraints(constraints)
    cnf = CNF(from_clauses=cnf_clauses)
    
    # Add blocking clauses for known solution
    blocking = create_blocking_clauses(var_mapping, puzzle.grid)
    cnf.extend(blocking)
    
    # Check for alternative solutions
    with Glucose3(cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            # Convert SAT solution back to grid
            alt_solution = [[False] * puzzle.width for _ in range(puzzle.height)]
            for (x, y), var in var_mapping.items():
                alt_solution[y][x] = model[var-1] > 0
            return False, alt_solution
    return True, None 