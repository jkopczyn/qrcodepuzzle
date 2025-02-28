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

from typing import List
from mosaic_puzzle import MosaicPuzzle
from puzzle_simplifier import simplify_puzzle

def load_count_grid(filename: str) -> List[List[int]]:
    grid: List[List[int]] = []
    with open(filename) as f:
        for line in f:
            row: List[int] = []
            for c in line.strip():
                if c == '-':
                    row.append(-1)
                else:
                    row.append(int(c))
            grid.append(row)
    return grid

if __name__ == "__main__":
    existing_puzzle = load_count_grid('count_grid.txt')
    # Convert count grid to MosaicPuzzle
    width: int = len(existing_puzzle[0])
    height: int = len(existing_puzzle)
    grid: List[List[bool]] = [[False] * width for _ in range(height)]  # Initial grid doesn't matter for simplification
    puzzle: MosaicPuzzle = MosaicPuzzle(width, height, grid, existing_puzzle)
    simplified = simplify_puzzle(puzzle)