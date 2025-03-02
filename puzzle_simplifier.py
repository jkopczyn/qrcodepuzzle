import copy
import random
from typing import List, Tuple

import file_io
from mosaic_puzzle import MosaicPuzzle
import uniqueness_checker

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

def simplify_puzzle(puzzle: MosaicPuzzle, clue_order: List[Tuple[int, int]] = None) -> Tuple[MosaicPuzzle, List[Tuple[int, int]]]:
    """
    Remove unnecessary clues while maintaining unique solvability.
    Returns simplified puzzle.
    """
    simplified = copy.deepcopy(puzzle)

    if clue_order is None:
        # Remove clues in random order, but set an order
        clue_order = randomize_clue_order(puzzle)

    if len(clue_order) == 0:
        print("No more clues to remove")
        print(simplified.grid, simplified.clues, simplified.original_clues)
        return (simplified, None)

    # Try removing this clue
    x, y = clue_order.pop()
    simplified.clues[y][x] = None

    # Check if still unique
    is_unique, alt_solution = uniqueness_checker.check_uniqueness(simplified)
    if not is_unique:
        # Restore clue if needed for uniqueness
        simplified.restore_clue(x, y)
        print("Restoring clue {} at ({}, {})".format(simplified.original_clues[y][x], x, y))

    return (simplified, clue_order)

def randomize_clue_order(puzzle: MosaicPuzzle) -> List[Tuple[int, int]]:
    clue_positions: List[Tuple[int, int]] = [(x, y)
                         for y in range(puzzle.height)
                         for x in range(puzzle.width)
                         if puzzle.clues[y][x] is not None]
    random.shuffle(clue_positions)
    return clue_positions

def deduplicate_count_grid(count_grid_filename: str, bool_grid_filename: str) -> MosaicPuzzle:
    puzzle: MosaicPuzzle = MosaicPuzzle.from_file(count_grid_filename, bool_grid_filename)
    print("Starting puzzle: {}".format(puzzle.clues))
    if not uniqueness_checker.check_validity(puzzle):
        print("Puzzle has no solution, cannot simplify")
        return puzzle
    else:
        print("Puzzle has a solution, simplifying")
    clue_order = randomize_clue_order(puzzle)
    print(clue_order)
    for i in range(puzzle.width * puzzle.height):
        simplified, clue_order = simplify_puzzle(puzzle, clue_order)
        print("before: {}\n after: {}".format(puzzle.clues, simplified.clues))
        # if simplified.clues == puzzle.clues:
        #     break
        puzzle = simplified
    return puzzle

if __name__ == "__main__":
    import sys
    count_grid_file, bool_grid_file, output_file = 'count_grid.txt', 'bool_grid.txt', 'deduplicated_count_grid.txt'
    if len(sys.argv) > 1:
        count_grid_file = sys.argv[1]
    if len(sys.argv) > 2:
        bool_grid_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    puzzle = deduplicate_count_grid(count_grid_file, bool_grid_file)
    file_io.save_count_grid(puzzle.clues, output_file)