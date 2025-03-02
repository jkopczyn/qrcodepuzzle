import copy
from pysat.formula import CNF
from pysat.solvers import Glucose3
from typing import List, Dict, Tuple

from process_count_grid import grid_to_constraints
from sat_problems import create_multiple_eqN_constraints, create_constraints_from_puzzle
from mosaic_puzzle import MosaicPuzzle
import uniqueness_checker

def debug_comparison(puzzle: MosaicPuzzle):
    """Compare the execution paths of check_validity and test_cnf"""
    print("=== ORIGINAL PUZZLE ===")
    print(f"Clues: {puzzle.clues}")
    print(f"Grid: {puzzle.grid}")
    
    # Path 1: check_validity approach
    print("\n=== CHECK_VALIDITY PATH ===")
    
    # Follow check_validity execution
    constraints1, var_mapping1 = grid_to_constraints(puzzle.clues)
    print(f"Constraints from grid_to_constraints: {constraints1}")
    print(f"Variable mapping: {var_mapping1}")
    
    cnf_clauses1, _ = create_multiple_eqN_constraints(constraints1)
    print(f"CNF clauses count: {len(cnf_clauses1)}")
    print(f"First 5 clauses: {cnf_clauses1[:5]}")
    
    cnf1 = CNF(from_clauses=cnf_clauses1)
    
    # Path 2: test_cnf approach
    print("\n=== TEST_CNF PATH ===")
    
    # Follow test_cnf execution
    clauses2, var_mapping2 = create_constraints_from_puzzle(puzzle.clues)
    print(f"CNF clauses count from create_constraints_from_puzzle: {len(clauses2)}")
    print(f"First 5 clauses: {clauses2[:5]}")
    print(f"Variable mapping: {var_mapping2}")
    
    # Compare the actual solutions
    print("\n=== COMPARING SOLUTIONS ===")
    # Solve with path 1
    with Glucose3(cnf1) as solver:
        success1 = solver.solve()
        print(f"Path 1 (check_validity) found solution: {success1}")
        if success1:
            model1 = solver.get_model()
            true_vars1 = [i for i in range(1, len(model1)+1) if model1[i-1] > 0]
            print(f"True variables: {true_vars1[:10]}{'...' if len(true_vars1) > 10 else ''}")
    
    # Create CNF for path 2 and solve
    cnf2 = CNF(from_clauses=clauses2) if not isinstance(clauses2, CNF) else clauses2
    with Glucose3(cnf2) as solver:
        success2 = solver.solve()
        print(f"Path 2 (test_cnf) found solution: {success2}")
        if success2:
            model2 = solver.get_model()
            true_vars2 = [i for i in range(1, len(model2)+1) if model2[i-1] > 0]
            print(f"True variables: {true_vars2[:10]}{'...' if len(true_vars2) > 10 else ''}")
    
    # Compare clause sets
    print("\n=== CLAUSES COMPARISON ===")
    clauses_set1 = {tuple(sorted(clause)) for clause in cnf_clauses1}
    clauses_set2 = {tuple(sorted(clause)) for clause in clauses2}
    
    print(f"Path 1 unique clauses: {len(clauses_set1 - clauses_set2)}")
    print(f"Path 2 unique clauses: {len(clauses_set2 - clauses_set1)}")
    
    if clauses_set1 != clauses_set2:
        print("DIFFERENCE FOUND: Clause sets are not identical!")
        
        # Show some differences
        if clauses_set1 - clauses_set2:
            print(f"Example clauses in path 1 but not path 2: {list(clauses_set1 - clauses_set2)[:3]}")
        if clauses_set2 - clauses_set1:
            print(f"Example clauses in path 2 but not path 1: {list(clauses_set2 - clauses_set1)[:3]}")
    else:
        print("Clause sets are identical")

    # Check if the variable mappings are the same
    print("\n=== VARIABLE MAPPING COMPARISON ===")
    if var_mapping1 == var_mapping2:
        print("Variable mappings are identical")
    else:
        print("DIFFERENCE FOUND: Variable mappings are not identical!")
        # Find differences in keys
        keys1 = set(var_mapping1.keys())
        keys2 = set(var_mapping2.keys())
        if keys1 != keys2:
            print(f"Keys in mapping1 but not mapping2: {keys1 - keys2}")
            print(f"Keys in mapping2 but not mapping1: {keys2 - keys1}")
        
        # Find differences in values for common keys
        common_keys = keys1.intersection(keys2)
        different_values = {k: (var_mapping1[k], var_mapping2[k]) 
                           for k in common_keys if var_mapping1[k] != var_mapping2[k]}
        if different_values:
            print(f"Different values for common keys: {different_values}")

# Run the comparison
if __name__ == "__main__":
    # Load your puzzle
    count_grid_file, bool_grid_file = 'count_grid.txt', 'bool_grid.txt'
    puzzle = MosaicPuzzle.from_file(count_grid_file, bool_grid_file)
    debug_comparison(puzzle) 