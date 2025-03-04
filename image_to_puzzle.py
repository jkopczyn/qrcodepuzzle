import sys
import count_grid_to_puzzle_code
from mosaic_puzzle import MosaicPuzzle
from process_count_grid import encode_grid_as_tatham_string
import puzzle_simplifier
import qrcode_to_bool_grid
import bool_grid_to_count_grid
import file_io
import sat_problems


if __name__ == "__main__":
    image_filename = 'puzzle.png'
    if len(sys.argv) > 1:
        image_filename = sys.argv[1]
    bool_grid = qrcode_to_bool_grid.image_to_bool_grid(image_filename)
    count_grid = bool_grid_to_count_grid.bool_grid_to_count_grid(bool_grid)
    print(bool_grid)
    print(count_grid)
    file_io.save_count_grid(count_grid, 'count_grid.txt')
    file_io.save_boolean_grid(bool_grid, 'bool_grid.txt')
    puzzle = MosaicPuzzle.from_file('count_grid.txt', 'bool_grid.txt')
    clauses, var_mapping = sat_problems.create_constraints_from_puzzle(puzzle.clues)
    file_io.save_constraints(clauses, 'constraints.txt')
    file_io.save_var_mapping(var_mapping, 'var_mapping.txt')
    clause_count = sum(len(clause) for clause in clauses)
    sum_count_constraints = sum(map(sum, puzzle.clues))
    black, white = puzzle.count_squares()
    print("Puzzle size: {}x{}".format(puzzle.width, puzzle.height))
    print("Clause count: {}".format(clause_count))
    print("Black squares: {}, White squares: {}".format(black, white))
    print("Total of count constraints: {}".format(sum_count_constraints))
    deduplicated_puzzle = puzzle_simplifier.deduplicate_count_grid(puzzle)
    print(deduplicated_puzzle.clues)
    file_io.save_count_grid(deduplicated_puzzle.clues, 'deduplicated_count_grid.txt')
    tatham_string = encode_grid_as_tatham_string(deduplicated_puzzle.clues)
    print("Puzzle URL: {}".format(count_grid_to_puzzle_code.PUZZLE_URL + tatham_string))
    print("Puzzle size: {}x{}".format(puzzle.width, puzzle.height))
    print("Clause count: {}".format(clause_count))
    print("Black squares: {}, White squares: {}".format(black, white))
    print("Total of count constraints: {}".format(sum_count_constraints))