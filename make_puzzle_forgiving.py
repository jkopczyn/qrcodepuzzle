
import random
import count_grid_to_puzzle_code
import file_io
from mosaic_puzzle import MosaicPuzzle
from process_count_grid import encode_grid_as_tatham_string


def replace_clues(puzzle: MosaicPuzzle, fraction_to_replace: float) -> MosaicPuzzle:
    missing_locations = [
        (x, y)
        for y in range(puzzle.height)
        for x in range(puzzle.width)
        if puzzle.clues[y][x] is None
    ]
    missing_count = len(missing_locations)
    target_count = int(missing_count * fraction_to_replace)
    print("{} clues blank, restoring {}".format(missing_count, target_count))
    for (x, y) in random.sample(missing_locations, target_count):
        puzzle.restore_clue(x, y)
    return puzzle


if __name__ == "__main__":
    import sys
    old_count_grid_file, new_count_grid_file = 'count_grid.txt', 'deduplicated_count_grid.txt'
    bool_grid_file, output_file = 'bool_grid.txt', 'forgiving_count_grid.txt'
    if len(sys.argv) > 1:
        old_count_grid_file = sys.argv[1]
    if len(sys.argv) > 2:
        new_count_grid_file = sys.argv[2]
    if len(sys.argv) > 3:
        bool_grid_file = sys.argv[3]
    if len(sys.argv) > 4:
        output_file = sys.argv[4]

    puzzle = MosaicPuzzle.from_file(old_count_grid_file, bool_grid_file)
    puzzle.clues = file_io.load_count_grid(new_count_grid_file)
    puzzle = replace_clues(puzzle, 0.5)
    puzzle.to_file(output_file)
    tatham_string = encode_grid_as_tatham_string(puzzle.clues)
    print(tatham_string)
    print("Puzzle URL: {}".format(count_grid_to_puzzle_code.PUZZLE_URL + tatham_string))