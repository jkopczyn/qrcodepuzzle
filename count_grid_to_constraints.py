from typing import List, Tuple, Dict
import file_io
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

def grid_to_constraints(grid: List[List[int]]) -> Tuple[List[Tuple[int, List[int]]], Dict[Tuple[int, int], int]]:
    """Convert a grid of count constraints into a list of (count, variables) tuples.

    Takes a grid where each cell contains a number, 0-9 or -1 to indicate a blank. For each number in the grid,
    creates a constraint tuple (N, vars) where N is the number and vars is a list of variable
    indices representing that cell and its 8 adjacent neighbors.

    Args:
        grid: 2D list where each cell contains an integer, 0-9 or -1 for a blank

    Returns:
        Tuple containing:
        - List of (N, vars) tuples where N is count and vars is list of variable indices
        - Dictionary mapping (x,y) positions to variable numbers
    """
    constraints: List[Tuple[int, List[int]]] = []
    var_mapping: Dict[Tuple[int, int], int] = {}
    
    # Create variable mapping first
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            var_mapping[(x,y)] = position_to_variable_int(grid, x, y)
            
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = grid[y][x]
            if c <= 0:  # Skip non-constraint cells
                continue

            # Get all positions within one step (including diagonals)
            neighbor_vars: List[int] = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    # re-use var_mapping
                    if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                        neighbor_vars.append(var_mapping[(nx,ny)])
            constraints.append((c, sorted(neighbor_vars)))

    return constraints, var_mapping

def position_to_variable_int(grid: List[List[int]], x: int, y: int) -> int:
    """Take x,y 0-indexed and return the number for the variable at that position in the grid.

    Args:
        grid: The puzzle grid
        x: x coordinate (column)
        y: y coordinate (row)

    Returns:
        Integer variable number (1-based) for the position
    """
    height = len(grid)
    width = len(grid[0])
    assert height == width
    return y * width + x + 1  # use row-major ordering

if __name__ == "__main__":
    count_grid = file_io.load_count_grid('count_grid.txt')
    constraints, var_mapping = grid_to_constraints(count_grid)
    print(constraints)
    file_io.save_constraints(constraints, 'constraints.txt')
    file_io.save_var_mapping(var_mapping, 'var_mapping.txt')
