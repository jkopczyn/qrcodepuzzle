# Example:
# 453
# 453
# 221

# Encode as a SAT problem using Sequential Counter encoding (de Jong 2023 p.19)
# each grid bool is a variable, e.g. grid[2,3] > c23
# each number clue is a count-true constraint, expressed as max-true plus a rider
#   e.g. 3 at grid[2,3] is max_3(c12, c13, c14, c22, c23, c24, c32, c33, c34) AND (rider_3)
# max_N/count_N are across M variables x_m, and use M segments of a tracker/counter; these are
#   tracked with new variables s_is, where variable x_1/x1 has variables s_1s for S from 1 to N
#   s21 represents that after including the value of variables x1...x2, 1 variable is true
# example: count_3 on 4 variables [x1, x2, x3, x4]; we have s11, s12, s13, s21, s22, ... s42, s43.
# This is encoded as:
# PROP01  (x1 -> s11) AND        # var1 starts counter if true
# PROP02  (s11 -> x1) AND        # rider: s11 *must* match x1
# PROP03  (x4 -> ~s33) AND       # max_3 constraint itself, if last var is true total must be <3 before it
# PROP04  (~s12 AND ~s13) AND    # impossible to have >1 true in 1 var
# PROP05  (s43) AND              # rider: the last variable must have exactly the right counter
#         (       # iterate for x_i from 1 < i < M
# PROP11  (x2 -> s21) AND  (x2 -> ~s13) AND   # as above, for var x2
# PROP12  (s11 -> s21) AND                    # if counter stands at 1 already it still does
# PROP13  (s21 -> (x2 OR s11)) AND            # rider: and s21 is only true if a prereq is met
#             (       # iterate for s_2j from 1 < j < N
# PROP21      ((x2 AND s11) -> s22) AND (s12 -> s22) AND  # counter stands at 2 if it was 2 or was 1 and +1
# PROP22      (s22 -> (x2 OR s12)) AND (s22 -> (s11 OR s12))  # rider: if and only if
#             ((x2 AND s12) -> s23) AND (s13 -> s23) AND  # continue up to max value of counter
#             (s23 -> (x2 OR s13)) AND (s23 -> (s12 OR s13))  # rider: also continue
#             )       # end iteration for s_2j from 1 < j < N
#         )       # end iteration for x_i from 1 < i < M
#         (x3 -> s31) AND  (x3 -> ~s23) AND
#         (s21 -> s31) AND
#         (s31 -> (x3 OR s21)) AND
#             (       # iterate
#             ((x3 AND s21) -> s32) AND (s22 -> s32) AND
#             (s32 -> (x3 OR s22)) AND (s32 -> (s21 OR s22))
#             ((x3 AND s22) -> s33) AND (s23 -> s33) AND
#             (s33 -> (x3 OR s23)) AND (s33 -> (s22 OR s23))
#             )       # end iteration
#         )       # end iteration
# PROPxy are handles to implement later

from pysat.formula import CNF
from pysat.solvers import Glucose3

def create_eqN_constraint(x_vars, n):
    """
    Creates an exactly-N constraint over the given x variables using sequential counter encoding.
    Returns (cnf_clauses, counter_vars) where counter_vars is a dict mapping (i,j) to variable numbers
    """
    cnf = []
    global nonce
    if 'nonce' not in globals():
        nonce = max(x_vars) + 1
    next_var = nonce
    nonce = next_var + (len(x_vars) * (n+1))  # Reserve space for all counter vars
    counter_vars = {}  # Maps (i,j) to variable number for s_ij
    
    # Create counter variables s_ij
    for i in range(1, len(x_vars) + 1):
        for j in range(1, n+1):  # Count up to n
            counter_vars[(i,j)] = next_var
            next_var += 1
    
    # For first variable (x1)
    # PROP01: (x1 -> s11)
    cnf.append([-x_vars[0], counter_vars[(1,1)]])
    # PROP02: (s11 -> x1)
    cnf.append([-counter_vars[(1,1)], x_vars[0]])
    # PROP04: (~s12 AND ~s13) - impossible to have >1 true in 1 var
    for i in range(2,n+1):
        cnf.append([-counter_vars[(1,i)]])
    
    # For middle variables
    for i in range(2, len(x_vars)):
        var_idx = i - 1  # Convert to 0-based index
        
        # PROP11: (xi -> si1) AND (xi -> ~s(i-1)3)
        cnf.append([-x_vars[var_idx], counter_vars[(i,1)]])
        cnf.append([-x_vars[var_idx], -counter_vars[(i-1,n)]])
        
        # PROP12: (s(i-1)1 -> si1)
        cnf.append([-counter_vars[(i-1,1)], counter_vars[(i,1)]])
        
        # PROP13: (si1 -> (xi OR s(i-1)1))
        cnf.append([-counter_vars[(i,1)], x_vars[var_idx], counter_vars[(i-1,1)]])
        
        # For each counter value j
        for j in range(2, n+1):
            # PROP21: ((xi AND s(i-1)(j-1)) -> sij) AND (s(i-1)j -> sij)
            cnf.append([-x_vars[var_idx], -counter_vars[(i-1,j-1)], counter_vars[(i,j)]])
            cnf.append([-counter_vars[(i-1,j)], counter_vars[(i,j)]])
            
            # PROP22: (sij -> (xi OR s(i-1)j)) AND (sij -> (s(i-1)(j-1) OR s(i-1)j))
            cnf.append([-counter_vars[(i,j)], x_vars[var_idx], counter_vars[(i-1,j)]])
            cnf.append([-counter_vars[(i,j)], counter_vars[(i-1,j-1)], counter_vars[(i-1,j)]])
    
    # For last variable (xn)
    last_i = len(x_vars)
    last_x = x_vars[-1]
    
    # Similar props as middle variables
    cnf.append([-last_x, counter_vars[(last_i,1)]])
    cnf.append([-counter_vars[(last_i-1,1)], counter_vars[(last_i,1)]])
    cnf.append([-counter_vars[(last_i,1)], last_x, counter_vars[(last_i-1,1)]])
    
    for j in range(2, n+1):
        # Add counter propagation for last variable
        cnf.append([-last_x, -counter_vars[(last_i-1,j-1)], counter_vars[(last_i,j)]])
        cnf.append([-counter_vars[(last_i-1,j)], counter_vars[(last_i,j)]])
        cnf.append([-counter_vars[(last_i,j)], last_x, counter_vars[(last_i-1,j)]])
        cnf.append([-counter_vars[(last_i,j)], counter_vars[(last_i-1,j-1)], counter_vars[(last_i-1,j)]])

    # PROP05: (sn3) - must have exactly 3 true
    cnf.append([counter_vars[(last_i,n)]])
    # PROP03: (xn -> ~s(n-1)3) - max_3 constraint
    cnf.append([-last_x, -counter_vars[(last_i-1,n)]])
    
    return cnf, counter_vars

def create_multiple_eqN_constraints(constraints):
    """
    Takes a list of (N, vars) tuples and returns a CNF encoding all constraints in conjunction.
    Each tuple specifies that exactly N of the variables must be True.

    Args:
        constraints: List of tuples (N, vars) where N is the count and vars is list of variable indices

    Returns:
        List of clauses representing the conjunction of all eq_N constraints
    """
    cnf = []
    counter_vars_list = []

    # Create eq_N constraint for each specification
    for n, x_vars in constraints:
        clauses, counter_vars = create_eqN_constraint(x_vars, n)
        cnf.extend(clauses)
        counter_vars_list.append(counter_vars)

    return cnf, counter_vars_list


# Example usage:
def test_eqN(n):
    # Create 5 variables (numbered 1-5)
    x_vars = list(range(1, n+2))
    
    cnf = CNF()
    clauses, counter_vars = create_eqN_constraint(x_vars, n)
    cnf.extend(clauses)
    result = test_cnf(cnf, x_vars)
    assert len(result) <= n, "More than {} variables are True!".format(n)

def test_cnf(cnf, vars):
    with Glucose3(cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            # Show which x variables are True
            result = [i for i in vars if model[i-1] > 0]
            print(f"Solution found: variables {result} are True")
            return result
        else:
            print("No solution found")

if __name__ == "__main__":
    test_eqN(3)
    test_eqN(5)
# Example:
# 453
# 453
# 221
# 4--
# -5-
# -2-
    max_possible_var = 1000  # Set this to whatever your maximum variable number might be
    clauses, counter_vars = create_multiple_eqN_constraints([
        (4, [1,2,4,5]),
        (5, [1,2,3,4,5,6,7,8,9]),
        (2, [4,5,6,7,8,9])
    ], start_nonce=max_possible_var + 1)
    print(clauses)
    test_cnf(clauses, list(range(1,10)))