# Example:
# 453
# 453
# 221
# to
# 4--
# -5-
# -2-

# Format in:
# 4--
# -5-
# -2-
# Format out:
# (4, [1,2,4,5]),
# (5, [1,2,3,4,5,6,7,8,9]),
# (2, [4,5,6,7,8,9])

def grid_to_constraints(grid):
    constraints = []
    for idx in range(len(grid)):
        row = grid[idx]
        for jdx in range(len(row)):
            c = row[jdx]
            digits = list(range(1,10))
            if c not in digits:
                continue
            # Get all positions within one step (including diagonals)
            neighbors = [
                (idx-1, jdx-1), (idx-1, jdx), (idx-1, jdx+1),
                (idx, jdx-1),   (idx, jdx),   (idx, jdx+1),
                (idx+1, jdx-1), (idx+1, jdx), (idx+1, jdx+1)
            ]
            # Filter valid positions and convert to variable numbers
            neighbor_vars = []
            for nx, ny in neighbors:
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    neighbor_vars.append(position_to_variable_int(grid, ny, nx))
            constraints.append((c, sorted(neighbor_vars)))
    return constraints

def position_to_variable_int(grid, x, y):
    """Take x,y 0-indexed and return the number for the variable at that position in the grid.
    """
    dim = len(grid)
    assert dim == len(grid[0])
    return (x+1) + dim*y

def load_count_grid(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            row = []
            for c in line.strip():
                if c == '-':
                    row.append(c)
                else:
                    row.append(int(c))
            grid.append(row)
    return grid

def save_constraints_to_file(constraints, filename):
    with open(filename, 'w') as f:
        for count, vars in constraints:
            f.write(f"({count}, {vars}),\n")

if __name__ == "__main__":
    count_grid = load_count_grid('count_grid.txt')
    constraints = grid_to_constraints(count_grid)
    print(constraints)
    save_constraints_to_file(constraints, 'constraints.txt')
