import sys
from typing import List
import file_io

def count_adjacent_ones(grid: List[List[bool]], row: int, col: int) -> int:
    count = 0
    height = len(grid)
    width = len(grid[0])

    # Check all 9 adjacent cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Check if adjacent cell is within grid bounds
            adj_row = row + i
            adj_col = col + j
            if 0 <= adj_row < height and 0 <= adj_col < width:
                # Count if adjacent cell is True (1)
                if grid[adj_row][adj_col]:
                    count += 1

    return count

def bool_grid_to_count_grid(bool_grid: List[List[bool]]) -> List[List[int]]:
    if not bool_grid or not bool_grid[0]:
        return []

    height: int = len(bool_grid)
    width: int = len(bool_grid[0])

    count_grid: List[List[int]] = []
    for row in range(height):
        count_row: List[int] = []
        for col in range(width):
            count_row.append(count_adjacent_ones(bool_grid, row, col))
        count_grid.append(count_row)
    return count_grid

def process_grid_files(input_filename: str, output_filename: str) -> None:
    """
    Processes a boolean grid file, converts it to a count grid, and saves the result.

    Args:
        input_file: Path to the input boolean grid file
        output_file: Path to save the output count grid
    """
    bool_grid = file_io.load_boolean_grid(input_filename)
    count_grid = bool_grid_to_count_grid(bool_grid)
    file_io.save_count_grid(count_grid, output_filename)

if __name__ == "__main__":
    # Default filenames
    input_file = 'bool_grid.txt'
    output_file = 'count_grid.txt'

    # Allow command-line arguments to override defaults
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    process_grid_files(input_file, output_file)
