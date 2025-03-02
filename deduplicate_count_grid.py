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
from typing import List, Tuple
from mosaic_puzzle import MosaicPuzzle
from puzzle_simplifier import simplify_puzzle, randomize_clue_order

def deduplicate_count_grid(count_grid_filename: str, bool_grid_filename: str) -> MosaicPuzzle:
    puzzle: MosaicPuzzle = MosaicPuzzle.from_file(count_grid_filename, bool_grid_filename)
    print("Starting puzzle: {}".format(puzzle.clues))
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
