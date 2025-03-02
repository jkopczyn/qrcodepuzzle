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

import file_io
from typing import List
from mosaic_puzzle import MosaicPuzzle
from puzzle_simplifier import simplify_puzzle

if __name__ == "__main__":
    existing_puzzle = file_io.load_count_grid('count_grid.txt')
    # Convert count grid to MosaicPuzzle
    width: int = len(existing_puzzle[0])
    height: int = len(existing_puzzle)
    grid: List[List[bool]] = [[False] * width for _ in range(height)]  # Initial grid doesn't matter for simplification
    puzzle: MosaicPuzzle = MosaicPuzzle(width, height, grid, existing_puzzle)
    print(puzzle.clues)
    for i in range(len(puzzle.clues)**2):
        simplified = simplify_puzzle(puzzle)
        print(simplified.clues)
        if simplified == puzzle:
            break
        puzzle = simplified
    file_io.save_count_grid(puzzle.clues, 'deduplicated_count_grid.txt')
