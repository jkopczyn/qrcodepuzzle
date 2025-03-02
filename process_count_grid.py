from typing import List, Tuple, Dict

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
            if c is None or c <= 0:  # Skip non-constraint cells
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

def encode_grid_as_tatham_string(grid: List[str]) -> str:
    if not grid or not grid[0]:
        return "#0x0:"
    height: int = len(grid)
    width: int = len(grid[0])
    if height != width:
        raise ValueError("Grid must be square")
    puzzle_string: str = f"#{height}x{width}:"
    current_blanks: int = 0

    # Flatten grid into sequence and convert strings to integers
    flattened: List[int] = []
    for row in grid:
        for cell in row:
            if cell == '-' or cell is None:
                flattened.append(-1)
            else:
                flattened.append(int(cell))

    for num in flattened:
        if num < 0:
            current_blanks += 1
            if current_blanks == 26:
                puzzle_string += 'z'
                current_blanks = 0
        else:
            if current_blanks > 0:
                puzzle_string += chr(ord('a') + current_blanks - 1)
                current_blanks = 0
            puzzle_string += str(num)

    if current_blanks > 0:
        puzzle_string += chr(ord('a') + current_blanks - 1)    
    return puzzle_string